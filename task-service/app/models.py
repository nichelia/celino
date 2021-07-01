import datetime
import uuid

from sqlalchemy import (ARRAY, CHAR, JSON, Column, DateTime, Float, ForeignKey,
                        Integer, MetaData, SmallInteger, String, Table,
                        TypeDecorator)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


task = Table(
    "task",
    MetaData(),
    Column("timestamp", Float, index=True),
    Column("state", String),
    Column("name", String, index=True),
    Column("routing_key", String),
    Column("uuid", GUID, primary_key=True),
    Column("retries", SmallInteger),
    Column("args", String),
    Column("kwargs", String),
    Column("result", String),
    Column("traceback", String),
    Column("result_meta", String),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)


state = Table(
    "state",
    MetaData(),
    Column("id", Integer, primary_key=True, index=True),
    Column("task_uuid", GUID, ForeignKey("task.uuid"), nullable=False),
    Column("timestamp", Float, index=True),
    Column("state", String),
    Column("result", String),
    Column("traceback", String),
    Column("result_meta", String),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)
