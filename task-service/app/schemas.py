from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class TaskBase(BaseModel):
    timestamp: Optional[float] = None
    state: Optional[str] = None
    name: Optional[str] = None
    routing_key: Optional[str] = None
    retries: Optional[int] = 0
    args: Optional[str] = None
    kwargs: Optional[str] = None
    result: Optional[str] = None
    traceback: Optional[str] = None
    result_meta: Optional[str] = None


# Properties to receive on item creation
class TaskCreate(TaskBase):
    name: str
    uuid: str


# Properties to receive on item update
class TaskUpdate(TaskBase):
    pass


# Properties shared by models stored in DB
class TaskInDBBase(TaskBase):
    name: str
    uuid: UUID


# Properties to return to client
class Task(TaskInDBBase):
    created_at: datetime
    updated_at: datetime
    pass


# Properties properties stored in DB
class TaskInDB(TaskInDBBase):
    pass