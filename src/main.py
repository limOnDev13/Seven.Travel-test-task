"""A module for building and launching an application."""

import logging.config
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from .config.app_config import Config
from .config.log_config import LOG_CONFIG
from .db.database import dependency_session, engine
from .db.models import Base
from .routes.tasks_route import router as task_router

config = Config()
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger("main_logger")

tags_metadata = [
    {
        "name": "Tasks",
        "description": "Operations with tasks.",
    },
]


@asynccontextmanager
async def lifespan(app_: FastAPI):
    """
    Add behavior before launching and after shutting down the app.

    The function adds data lifting before startup
    (as well as pre-reset data in debug mode).

    :param app_: FastAPI app.
    """
    logger.info("Start up.")

    async with engine.begin() as conn:
        if config.debug:
            logger.debug("Debug mode.")
            logger.warning("Drop db.")
            await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)

    yield

    logger.info("Shut down.")
    await engine.dispose()


def create_app() -> FastAPI:
    """Configure and create the FastAPI app."""
    logger.info("Creating FastAPI app...")
    app_ = FastAPI(
        lifespan=lifespan,
        openapi_tags=tags_metadata,
        dependencies=[Depends(dependency_session)],
    )

    app_.include_router(task_router)

    return app_


app: FastAPI = create_app()
