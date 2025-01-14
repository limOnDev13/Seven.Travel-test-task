"""The module responsible for testing endpoints from the module tasks_route.py."""

from typing import Any, Dict

import pytest
from httpx import AsyncClient

from src.schemas.schemas import TaskInSchema


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
