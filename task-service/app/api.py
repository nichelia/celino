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


@router.post("/", response_model=schemas.Task)
async def create_task(
    *,
    task_in: schemas.TaskCreate,
) -> Any:
    """
    Create new task.
    """
    task_id = await crud.task.create(obj_in=task_in)
    response = {
        'id': task_id,
        **task_in.dict()
    }
    return response


@router.get("/{id}", response_model=schemas.Task)
async def read_task(
    *,
    id: int,
) -> Any:
    """
    Read task by ID.
    """
    task = await crud.task.read(id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{id}", response_model=schemas.Task)
async def update_task(
    *,
    id: int,
    task_in: schemas.TaskUpdate,
) -> Any:
    """
    Update an task.
    """
    task = await crud.task.read(id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if isinstance(task_in, dict):
        update_data = task_in
    else:
        update_data = task_in.dict(exclude_unset=True)

    obj_in_db = schemas.TaskUpdate(**task)
    updated_obj = obj_in_db.copy(update=update_data)

    task = await crud.task.update(id=id, obj_in=updated_obj)
    response = {
        'id': id,
        **updated_obj.dict()
    }
    return response


@router.delete("/{id}", response_model=schemas.Task)
async def delete_task(
    *,
    id: int,
) -> Any:
    """
    Delete an task.
    """
    task = await crud.task.read(id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await crud.task.delete(id=id)
    return task