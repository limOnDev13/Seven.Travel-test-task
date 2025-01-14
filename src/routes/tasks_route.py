"""The module responsible for the endpoints related to the tasks."""

import json
from typing import List, Optional

from fastapi import APIRouter, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories import TaskRepository
from src.schemas.schemas import STATUSES, TaskInSchema, TaskOutSchema

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
        return await task_rep.get_all()
    elif status in STATUSES:
        return await task_rep.get_all_by_status(status)
    else:
        return Response(
            status_code=400,
            content=json.dumps({"msg": "Invalid status"}),
            media_type="application/json",
        )
