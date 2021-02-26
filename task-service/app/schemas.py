from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel


# Shared properties
class TaskBase(BaseModel):
    name: Optional[str] = None
    routing_key: Optional[str] = None
    uuid: Optional[str] = None
    retries: Optional[int] = 0
    args: Optional[List[str]] = None
    kwargs: Optional[Dict[Any, Any]] = None
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
    id: int
    # created_at: datetime
    # updated_at: datetime
    name: str
    uuid: str


# Properties to return to client
class Task(TaskInDBBase):
    pass


# Properties properties stored in DB
class TaskInDB(TaskInDBBase):
    pass