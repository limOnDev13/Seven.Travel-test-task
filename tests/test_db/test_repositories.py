"""The module responsible for testing repositories."""

from typing import List

import pytest

from src.db.repositories import TaskRepository
from src.schemas.schemas import TaskInSchema, TaskOutSchema


@pytest.mark.asyncio
async def test_task_repository_create(
    rep: TaskRepository, task_in: TaskInSchema
) -> None:
    try:
        task_id: int = await rep.create(task_in)
        assert task_id == 1
    except Exception as exc:
        pytest.fail(str(exc))


@pytest.mark.asyncio
async def test_task_repository_get(rep: TaskRepository, task_in: TaskInSchema) -> None:
    assert await rep.get(1) is None

    task_id: int = await rep.create(task_in)
    result = await rep.get(task_id)
    assert isinstance(result, TaskOutSchema)


@pytest.mark.asyncio
async def test_task_repository_get_all(
    rep: TaskRepository, many_task_in: List[TaskInSchema]
) -> None:
    for task in many_task_in:
        await rep.create(task)

    tasks_from_db: List[TaskOutSchema] = await rep.get_all()

    for task_from_db, task_ in zip(
        sorted(tasks_from_db, key=lambda data: data.title),
        sorted(many_task_in, key=lambda data: data.title),
    ):
        for key, value in task_:
            assert value == getattr(task_from_db, key)
