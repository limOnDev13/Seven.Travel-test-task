"""The module responsible for testing endpoints from the module tasks_route.py."""

from typing import Any, Dict, List

import pytest
from httpx import AsyncClient

from src.schemas.schemas import STATUSES, TaskInSchema


@pytest.mark.asyncio
async def test_post_tasks(client: AsyncClient, task_in: TaskInSchema) -> None:
    """Test the endpoint POST /tasks/."""
    response = await client.post("/tasks/", json=task_in.model_dump())
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_post_tasks_invalid_data(
    client: AsyncClient, task_in: TaskInSchema
) -> None:
    """Test the endpoint POST /tasks/ with invalid input data."""
    invalid_input_data: Dict[str, Any] = {"invalid": "data"}
    response = await client.post("/tasks/", json=invalid_input_data)
    assert response.status_code == 422

    invalid_input_data = task_in.model_dump()
    invalid_input_data["status"] = "invalid status"
    response = await client.post("/tasks/", json=invalid_input_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_all_tasks_without_status(
    client: AsyncClient, many_task_in: List[TaskInSchema]
):
    """Test the endpoint GET /tasks/ without status."""
    for task_in in many_task_in:
        response = await client.post("/tasks/", json=task_in.model_dump())
        assert response.status_code == 201

    response = await client.get("/tasks/")
    assert response.status_code == 200

    for task_from_server, task_from_test in zip(
        sorted(response.json(), key=lambda data: data["id"]), many_task_in
    ):
        for key, value in task_from_server.items():
            if key != "id":
                assert value == getattr(task_from_test, key)


@pytest.mark.asyncio
async def test_get_all_tasks_with_status(
    client: AsyncClient, many_task_in: List[TaskInSchema]
):
    """Test the endpoint GET /tasks/ with status."""
    for task_in in many_task_in:
        response = await client.post("/tasks/", json=task_in.model_dump())
        assert response.status_code == 201

    for status in STATUSES:
        response = await client.get(f"/tasks/?status={status}")
        assert response.status_code == 200

        for task_from_server, task_from_test in zip(
            sorted(response.json(), key=lambda data: data["id"]),
            [
                task_with_status
                for task_with_status in many_task_in
                if task_with_status.status == status
            ],
        ):
            for key, value in task_from_server.items():
                if key != "id":
                    assert value == getattr(task_from_test, key)


@pytest.mark.asyncio
async def test_get_all_tasks_with_invalid_status(
    client: AsyncClient, many_task_in: List[TaskInSchema]
):
    """Test the endpoint GET /tasks/ with invalid status."""
    for task_in in many_task_in:
        response = await client.post("/tasks/", json=task_in.model_dump())
        assert response.status_code == 201

    status: str = "invalid status"
    response = await client.get(f"/tasks/?status={status}")
    assert response.status_code == 400
