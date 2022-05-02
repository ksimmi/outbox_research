import asyncio
import json
from nats.aio.client import Client as NATS


class NATSPublisher:

    def __init__(self):
        self.values = {
            "aggregate_type": "SomeAggr",
            "aggregate_id": "some-id",
            "type": "some-type",
            "payload": {
                "key": "value"
            }
        }


    def __await__(self):
        async def publisher():
            nc = NATS()
            await nc.connect("nats://localhost:4222")

            for i in range(1, 1000000):
                await asyncio.sleep(1)
                self.values['payload'] = dict(counter=i)
                await nc.publish("help", json.dumps(self.values).encode())

            nc.close()


        return publisher().__await__()

# async def client():
#     nc = NATS()
#     await nc.connect("nats://localhost:4222")
#
#     for i in range(1, 1000000):
#         await asyncio.sleep(1)
#         values['payload'] = dict(counter=i)
#         await nc.publish("help", json.dumps(values).encode())
#
#     nc.close()
