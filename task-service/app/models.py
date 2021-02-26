import datetime

from sqlalchemy import (
    ARRAY,
    Column,
    DateTime,
    Integer,
    JSON,
    MetaData,
    String,
    Table,
)


task = Table(
    "task",
    MetaData(),
    Column("id", Integer, primary_key=True, index=True),
    Column("created_at", DateTime, default=datetime.datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.datetime.utcnow),
    Column("name", String, index=True),
    Column("routing_key", String),
    Column("uuid", String),
    Column("retries", Integer),
    Column("args", ARRAY(String)),
    Column("kwargs", JSON),
    Column("result", String),
    Column("traceback", String),
    Column("result_meta", String),
)