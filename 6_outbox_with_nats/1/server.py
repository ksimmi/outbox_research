import asyncio
import json
import signal
from nats.aio.client import Client as NATS

from subscribers import Subscriber

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


    # Use queue named 'workers' for distributing requests
    # among subscribers.
    await nc.subscribe(*Subscriber())