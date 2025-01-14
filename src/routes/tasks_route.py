"""The module responsible for the endpoints related to the tasks."""

import json
import logging
from typing import List, Optional

from fastapi import APIRouter, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories import TaskRepository
from src.schemas.schemas import STATUSES, TaskInSchema, TaskOutSchema

logger = logging.getLogger("main_logger.router")

router: APIRouter = APIRouter(
    tags=["tasks"],
)


@router.post(
    "/tasks/",
    status_code=201,
    responses={
        201: {
            "description": "A task was created",
            "content": {"application/json": {"example": {"msg": "OK", "task_id": 1}}},
        },
    },
)
async def create_task(request: Request, task: TaskInSchema):
    """Create a new task."""
    session: AsyncSession = request.state.session
    task_rep: TaskRepository = TaskRepository(session)
    task_id: int = await task_rep.create(task)

    logger.info("Created a new task with id %d", task_id)

    return {"msg": "OK", "task_id": task_id}


@router.get(
    "/tasks/",
    status_code=200,
    response_model=List[TaskOutSchema],
    responses={
        400: {
            "description": "Not such status.",
            "content": {"application/json": {"example": {"msg": "Invalid status"}}},
        },
    },
)
async def get_all_tasks(request: Request, status: Optional[str] = None):
    """Get all tasks (or all tasks with the status)."""
    session: AsyncSession = request.state.session
    task_rep: TaskRepository = TaskRepository(session)

    if status is None:
        logger.info("Returned all tasks.")
        return await task_rep.get_all()
    elif status in STATUSES:
        logger.info("Returned all tasks with status %s.", status)
        return await task_rep.get_all_by_status(status)
    else:
        logger.warning("Invalid status received.")
        return Response(
            status_code=400,
            content=json.dumps({"msg": "Invalid status"}),
            media_type="application/json",
        )


@router.get(
    "/tasks/{idx}/",
    status_code=200,
    response_model=TaskOutSchema,
    responses={
        404: {
            "description": "Task not found.",
            "content": {"application/json": {"example": {"msg": "Not found"}}},
        },
    },
)
async def get_task(request: Request, idx: int):
    """Get task by id."""
    session: AsyncSession = request.state.session
    task_rep: TaskRepository = TaskRepository(session)

    result: Optional[TaskOutSchema] = await task_rep.get(idx)
    if result is None:
        logger.warning("Task with id %d not found.", idx)
        return Response(
            status_code=404,
            content=json.dumps({"msg": "Not found"}),
            media_type="application/json",
        )

    logger.info("Return the task with id %d", idx)
    return result


@router.put(
    "/tasks/{idx}/",
    status_code=200,
    responses={
        200: {
            "description": "Task was updated.",
            "content": {"application/json": {"example": {"msg": "OK"}}},
        },
        404: {
            "description": "Task not found.",
            "content": {"application/json": {"example": {"msg": "Not found"}}},
        },
    },
)
async def update_task(request: Request, idx: int, task_in: TaskInSchema):
    """Update the task."""
    session: AsyncSession = request.state.session
    task_rep: TaskRepository = TaskRepository(session)

    try:
        await task_rep.update(idx, task_in)
        logger.info("The task with id %d was updated.", idx)
        return {"msg": "OK"}
    except ValueError:
        logger.warning("Task with id %d not found.", idx)
        return Response(
            status_code=404,
            content=json.dumps({"msg": "Not found"}),
            media_type="application/json",
        )


@router.delete(
    "/tasks/{idx}/",
    status_code=202,
    responses={
        202: {
            "description": "Task was deleted.",
            "content": {"application/json": {"example": {"msg": "OK"}}},
        },
        404: {
            "description": "Task not found.",
            "content": {"application/json": {"example": {"msg": "Not found"}}},
        },
    },
)
async def delete_task(request: Request, idx: int):
    """Delete the task."""
    session: AsyncSession = request.state.session
    task_rep: TaskRepository = TaskRepository(session)

    try:
        await task_rep.delete(idx)
        logger.info("Task with id %d was deleted.", idx)
        return {"msg": "OK"}
    except ValueError:
        logger.warning("Task with id %d not found.", idx)
        return Response(
            status_code=404,
            content=json.dumps({"msg": "Not found"}),
            media_type="application/json",
        )
