import asyncio as aio
import os
import signal
from nats.aio.client import Client as NATS


def greet_user():
    str = input('type something and press Enter: ')
    print(str)


tasks = []


async def main():


    async def client():
        nc = NATS()
        inbox = nc.new_inbox()

        await nc.connect(servers=["nats://localhost:4222"])
        await nc.publish("help", b'Hello', reply=inbox)
        await nc.publish("help", b'World', reply=inbox)
        await nc.publish("help", b'!!!!!', reply=inbox)
        await nc.close()


    async def server():
        nc = NATS()

        async def closed_cb():
            print("Connection to NATS is closed.")
            await aio.sleep(0.1)
            aio.get_running_loop().stop()

        options = {
            "servers": ["nats://localhost:4222"],
            "closed_cb": closed_cb
        }

        await nc.connect(**options)
        print(f"Connected to NATS at {nc.connected_url.netloc}...")

        async def subscribe_handler(msg):
            subject = msg.subject
            reply = msg.reply
            data = msg.data.decode()
            print("Received a message on '{subject} {reply}': {data}".format(
                subject=subject, reply=reply, data=data))
            await msg.respond(b'I can help!')

        # Basic subscription to receive all published messages
        # which are being sent to a single topic 'discover'
        await nc.subscribe("help", cb=subscribe_handler)

        # Subscription on queue named 'workers' so that
        # one subscriber handles message a request at a time.
        await nc.subscribe("help.*", "workers", subscribe_handler)

        def signal_handler():
            if nc.is_closed:
                return
            print("Disconnecting...")
            aio.create_task(nc.close())

        for sig in ('SIGINT', 'SIGTERM'):
            aio.get_running_loop().add_signal_handler(getattr(signal, sig), signal_handler)

        await nc.request("help", b'help')

        await aio.sleep(1)


    tasks.append(aio.create_task(server()))
    # tasks.append(aio.create_task(client()))
    await aio.gather(*tasks)


if __name__ == '__main__':
    try:
        aio.run(main())
    except:
        pass