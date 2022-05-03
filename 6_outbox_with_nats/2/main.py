import asyncio
from client import NATSPublisher
from server import NATSServer
from subscribers import HELP_SUBSCRIBER

async def nats_server():
    await NATSServer(
        subscribers=[
            HELP_SUBSCRIBER,
        ]
    )

async def pub():
    await NATSPublisher()

async def main(tasks=[]):
    tasks.append(asyncio.create_task(pub()))
    tasks.append(asyncio.create_task(nats_server()))

    asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_forever()
        loop.close()
    except:
        pass

