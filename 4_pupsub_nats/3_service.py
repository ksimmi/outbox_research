import asyncio
import signal

from nats.aio.client import Client as NATS

tasks = []

async def greet_user():
    str = input('type something and press Enter: ')
    yield

async def main():

    async def client():
        nc = NATS()
        await nc.connect("nats://localhost:4222")

        # while True:
        #     str = input('type something and press Enter: ').encode()
        #     try:
        #         response = await nc.request("help", str)
        #         print(response)
        #     except Exception as e:
        #         print("Error:", e)

        for i in range(1, 1000000):
            await asyncio.sleep(1)
            try:
                response = await nc.request("help", b'hi')
                print(response)
            except Exception as e:
                print("Error:", e)

        nc.close()

    async def server():
        nc = NATS()

        async def stop():
            await asyncio.sleep(1)
            asyncio.get_running_loop().stop()

        def signal_handler():
            if nc.is_closed:
                return
            print("Disconnecting...")
            asyncio.create_task(nc.close())
            asyncio.create_task(stop())

        for sig in ('SIGINT', 'SIGTERM'):
            asyncio.get_running_loop().add_signal_handler(getattr(signal, sig), signal_handler)

        async def disconnected_cb():
            print("Got disconnected...")

        async def reconnected_cb():
            print("Got reconnected...")

        await nc.connect("nats://localhost:4222",
                         reconnected_cb=reconnected_cb,
                         disconnected_cb=disconnected_cb,
                         max_reconnect_attempts=-1)

        async def help_request(msg):
            subject = msg.subject
            reply = msg.reply
            data = msg.data.decode()
            print("Received a message on '{subject} {reply}': {data}".format(
                subject=subject, reply=reply, data=data))
            await nc.publish(reply, b'I can help')

        # Use queue named 'workers' for distributing requests
        # among subscribers.
        await nc.subscribe("help", "workers", help_request)

    tasks.append(asyncio.create_task(client()))
    tasks.append(asyncio.create_task(server()))

    asyncio.gather(*tasks)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_forever()
        loop.close()
    except:
        pass