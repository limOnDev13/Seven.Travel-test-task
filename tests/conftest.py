"""The module responsible for the fixtures for the tests."""

import random
from string import ascii_letters
from typing import AsyncGenerator, Callable, Generator, List

import pytest
import pytest_asyncio
from fastapi import FastAPI, Request
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import Session, engine
from src.db.models import Base
from src.db.repositories import TaskRepository
from src.main import create_app
from src.schemas.schemas import STATUSES, TaskInSchema


@pytest_asyncio.fixture()
async def db() -> AsyncGenerator[None, None]:
    """Drop and raise the base before each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


@pytest_asyncio.fixture()
async def session(db) -> AsyncGenerator[AsyncSession, None]:
    """Wrap queries in a transaction and return the session object."""
    async with Session() as session_:
        try:
            yield session_
        except Exception as exc:
            await session_.rollback()
            raise exc


@pytest.fixture
def rep(session: AsyncSession) -> Generator[TaskRepository, None, None]:
    """Return the TaskRepository object."""
    yield TaskRepository(session)


@pytest.fixture
def task_in() -> Generator[TaskInSchema, None, None]:
    """Return the TaskInSchema object."""
    yield TaskInSchema(
        title="Test Title",
        description="Test Description",
        status=random.choice(list(STATUSES)),
    )


@pytest.fixture
def updated_task_in() -> Generator[TaskInSchema, None, None]:
    """Return the TaskInSchema object."""
    yield TaskInSchema(
        title="Updated Test Title",
        description="Updated Test Description",
        status=random.choice(list(STATUSES)),
    )


@pytest.fixture
def many_task_in() -> Generator[List[TaskInSchema], None, None]:
    """Return many TaskInSchema objects."""
    yield [
        TaskInSchema(
            title="".join(random.choices(ascii_letters, k=random.randint(1, 10))),
            description="".join(
                random.choices(ascii_letters, k=random.randint(1, 100))
            ),
            status=random.choice(list(STATUSES)),
        )
        for _ in range(random.randint(10, 100))
    ]


@pytest_asyncio.fixture(scope="function")
async def dependency_session(session: AsyncSession) -> AsyncGenerator[Callable, None]:
    """Start a test database session."""

    async def overrides_get_session(request: Request):
        request.state.session = session
        yield

    yield overrides_get_session
    await session.close()


@pytest.fixture(scope="function")
def test_app(dependency_session: Callable) -> Generator[FastAPI, None, None]:
    """Create a test_app with overridden dependencies."""
    _app: FastAPI = create_app()
    _app.dependency_overrides[dependency_session] = dependency_session
    yield _app
    _app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create a http client."""
    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://localhost:8000"
    ) as client:
        yield client
