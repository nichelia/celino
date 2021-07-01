from typing import Any, List, Generator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app._version import __version__
from app import crud, models, schemas
from app.db import asyncSession


router = APIRouter()


@router.get("/version", response_class=JSONResponse)
def version():
    version = {"version": __version__}
    return JSONResponse(status_code=200, content=version)


@router.get("/", response_model=List[schemas.Task])
async def read_tasks() -> Any:
    """
    Read tasks.
    """
    tasks = await crud.task.read_all()
    return tasks


@router.post("/", response_model=schemas.TaskCreate)
async def create_task(
    *,
    task_in: schemas.TaskCreate,
) -> Any:
    """
    Create new task.
    """
    await crud.task.create(obj_in=task_in)
    response = task_in.dict()
    return response


@router.get("/{uuid}", response_model=schemas.Task)
async def read_task(
    *,
    uuid: str,
) -> Any:
    """
    Read task by UUID.
    """
    task = await crud.task.read(uuid=uuid)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{uuid}", response_model=schemas.TaskUpdate)
async def update_task(
    *,
    uuid: str,
    task_in: schemas.TaskUpdate,
) -> Any:
    """
    Update an task.
    """
    task = await crud.task.read(uuid=uuid)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if isinstance(task_in, dict):
        update_data = task_in
    else:
        update_data = task_in.dict(exclude_unset=True)

    obj_in_db = schemas.TaskUpdate(**task)
    updated_obj = obj_in_db.copy(update=update_data)

    task = await crud.task.update(uuid=uuid, obj_in=updated_obj)
    response = {
        'uuid': uuid,
        **updated_obj.dict()
    }
    return response


@router.delete("/{uuid}", response_model=schemas.Task)
async def delete_task(
    *,
    uuid: str,
) -> Any:
    """
    Delete an task.
    """
    task = await crud.task.read(uuid=uuid)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await crud.task.delete(uuid=uuid)
    return task