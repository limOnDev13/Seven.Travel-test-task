"""The module responsible for the endpoints related to the tasks."""

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories import TaskRepository
from src.schemas.schemas import TaskInSchema

router: APIRouter = APIRouter()
templates = Jinja2Templates(directory="templates")


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
