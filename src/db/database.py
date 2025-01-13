"""The module responsible for configuring the connection to the database."""

from logging import getLogger
from typing import Callable

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.config.app_config import Config

logger = getLogger("main.db")

db_config = Config().db

engine: AsyncEngine = create_async_engine(db_config.url)
Session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


def connection(func: Callable):
    """Add a session to the func as an argument for working with the db."""

    async def wrapper(*args, **kwargs):
        """Wrap the func."""
        async with Session() as session:
            try:
                return await func(*args, session=session, **kwargs)
            except Exception as exc:
                logger.exception(str(exc))
                await session.rollback()
                raise exc

    return wrapper
