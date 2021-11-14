from sqlalchemy import create_engine, text
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID

engine = create_engine('postgresql://postgres:qwerty@localhost/outbox_research', echo=True, future=True)
metadata = MetaData()

Outbox = Table(
    "outbox",
    metadata,
    Column('id', UUID, primary_key=True, server_default=text("uuid_generate_v4()")),
    Column('aggregate_type', String),
    Column('aggregate_id', String),
    Column('type', String),
    Column('payload', JSON),
)

