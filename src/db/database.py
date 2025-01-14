"""The module responsible for configuring the connection to the database."""

from logging import getLogger
from typing import Any, AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config.app_config import Config

logger = getLogger("main.db")

db_config = Config().db

engine: AsyncEngine = create_async_engine(db_config.url)
Session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def dependency_session(request: Request) -> AsyncGenerator[AsyncSession, Any]:
    """Create a transaction and save session obj to request.state.session."""
    async with Session() as session_:
        try:
            request.state.session = session_
            yield session_
        except Exception as exc:
            logger.exception(str(exc))
            await session_.rollback()
            raise exc
