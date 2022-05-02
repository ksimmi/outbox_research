import asyncio
import signal
import json
from nats.aio.client import Client as NATS

from sqlalchemy import insert
from schema import engine, tOutbox

#
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
#
#
# async def server():
#     nc = NATS()
#
#     async def stop():
#         await asyncio.sleep(1)
#         asyncio.get_running_loop().stop()
#
#     def signal_handler():
#         if nc.is_closed:
#             return
#         print("Disconnecting...")
#         asyncio.create_task(nc.close())
#         asyncio.create_task(stop())
#
#     for sig in ('SIGINT', 'SIGTERM'):
#         asyncio.get_running_loop().add_signal_handler(getattr(signal, sig), signal_handler)
#
#     async def disconnected_cb():
#         print("Got disconnected...")
#
#     async def reconnected_cb():
#         print("Got reconnected...")
#
#     await nc.connect("nats://localhost:4222",
#                      reconnected_cb=reconnected_cb,
#                      disconnected_cb=disconnected_cb,
#                      max_reconnect_attempts=-1)
#
#     async def help_request(msg):
#         data = json.loads(msg.data.decode())
#
#         print(data)
#         insert_values(data)
#         # await nc.publish(reply, b'I can help')
#
#     # Use queue named 'workers' for distributing requests
#     # among subscribers.
#     await nc.subscribe("help", "workers", help_request)
#
#
# async def main(tasks=[]):
#     tasks.append(asyncio.create_task(client()))
#     tasks.append(asyncio.create_task(server()))
#
#     asyncio.gather(*tasks)
#
#
# if __name__ == '__main__':
#     loop = asyncio.new_event_loop()
#     try:
#         loop.run_until_complete(main())
#         loop.run_forever()
#         loop.close()
#     except:
#         pass