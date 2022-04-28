from sqlalchemy import insert

from schema import engine, tOutbox

with engine.begin() as conn:
    conn.execute(
        insert(tOutbox).values(
            aggregate_type="SomeAggr",
            aggregate_id="some-id",
            type="some-type",
            payload={
                "key": "value"
            }
        )
    )