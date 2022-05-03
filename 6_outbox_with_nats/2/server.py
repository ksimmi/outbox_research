import asyncio
import json
import signal
from nats.aio.client import Client as NATS

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


async def disconnected_cb():
    print("Got disconnected...")


async def reconnected_cb():
    print("Got reconnected...")


class NATSServer:

    def __init__(self, subscribers=[]):
        self.subscribers = subscribers

    def __await__(self):
        async def server(subscribers=[]):

            for stop_signal in ('SIGINT', 'SIGTERM'):
                asyncio.get_running_loop().add_signal_handler(getattr(signal, stop_signal), signal_handler)

            await nc.connect("nats://localhost:4222",
                             reconnected_cb=reconnected_cb,
                             disconnected_cb=disconnected_cb,
                             max_reconnect_attempts=-1)

            tasks = []
            for subscriber in subscribers:
                tasks.append(
                    asyncio.create_task(
                        nc.subscribe(*subscriber)))

            asyncio.gather(*tasks)

        return server(self.subscribers).__await__()


