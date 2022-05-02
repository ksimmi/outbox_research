import asyncio
from client import NATSPublisher
from server import server

async def pub():
    await NATSPublisher()

async def main(tasks=[]):
    tasks.append(asyncio.create_task(pub()))
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