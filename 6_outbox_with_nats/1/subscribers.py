import json

from sqlalchemy import insert
from schema import engine, tOutbox

def insert_values(values):
    with engine.begin() as conn:
        conn.execute(
            insert(tOutbox).values(**values)
        )

async def help_request(msg):
    data = json.loads(msg.data.decode())

    print(data)
    insert_values(data)
    # await nc.publish(reply, b'I can help')


class Subscriber:
    subject = 'help'
    group = 'workers'
    callback = help_request

    def __new__(self):
        return [self.subject, self.group, self.callback]
