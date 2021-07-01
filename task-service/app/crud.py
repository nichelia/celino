from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models import task
from app.schemas import Task, TaskCreate, TaskUpdate
from app.db import session, asyncSession


ReturnSchemaType = TypeVar("ReturnSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ReturnSchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ReturnSchemaType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A Pydantic model (schema) class
        """
        self.model = model

    async def read_all(self) -> List[ReturnSchemaType]:
        query = self.model.select()
        return await asyncSession.fetch_all(query=query)

    async def create(self, *, obj_in: CreateSchemaType) -> ReturnSchemaType:
        obj_in_data = jsonable_encoder(obj_in)
        query = self.model.insert().values(**obj_in_data)
        return await asyncSession.execute(query=query)

    async def read(self, uuid: str) -> Optional[ReturnSchemaType]:
        query = self.model.select(self.model.c.uuid == uuid)
        return await asyncSession.fetch_one(query=query)

    async def update(
        self,
        *,
        uuid: str,
        obj_in: UpdateSchemaType
    ) -> ReturnSchemaType:
        query = (
            self.model
            .update()
            .where(self.model.c.uuid == uuid)
            .values(**obj_in.dict())
        )
        return await asyncSession.execute(query=query)

    async def delete(self, *, uuid: str) -> ReturnSchemaType:
        query = (
            self.model
            .delete()
            .where(self.model.c.uuid == uuid)
        )
        return await asyncSession.execute(query=query)


task = CRUDBase[Task, TaskCreate, TaskUpdate](task)