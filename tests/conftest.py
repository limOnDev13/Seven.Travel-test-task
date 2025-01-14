"""The module responsible for the fixtures for the tests."""

from typing import AsyncGenerator, Generator, List
import random
from string import ascii_letters

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Base
from src.db.database import engine, Session
from src.db.repositories import TaskRepository
from src.schemas.schemas import TaskInSchema, STATUSES


@pytest_asyncio.fixture()
async def db() -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


@pytest_asyncio.fixture()
async def session(db) -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session_:
        try:
            yield session_
        except Exception as exc:
            await session_.rollback()
            raise exc


@pytest.fixture
def rep(session: AsyncSession) -> Generator[TaskRepository, None, None]:
    yield TaskRepository(session)


@pytest.fixture
def task_in() -> Generator[TaskInSchema, None, None]:
    yield TaskInSchema(
        title="Test Title",
        description="Test Description",
        status=random.choice(list(STATUSES)),
    )


@pytest.fixture
def many_task_in() -> Generator[List[TaskInSchema], None, None]:
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
