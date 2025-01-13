"""The module responsible for database queries."""

from typing import List, Optional, Type

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.schemas import TaskInSchema, TaskOutSchema

from .database import Base
from .models import Task


class BaseRepository(object):
    """
    Base repository.

    Args:
        session (AsyncSession) - async session object.
    """

    orm_model: Type[Base] = Base
    schema_in: Type[BaseModel] = BaseModel
    schema_out: Type[BaseModel] = BaseModel
    not_found_error_str: str = "Item not found"

    def __init__(self, session: AsyncSession):
        """Initialize class."""
        self.__session = session

    async def create(self, data: schema_in) -> int:
        """Create a new item."""
        new_item = self.orm_model(data.model_dump())
        self.__session.add(new_item)
        await self.__session.commit()
        return new_item.id

    async def get_all(self) -> List[schema_out]:
        """Get all items."""
        items_q = await self.__session.execute(select(self.orm_model))
        return [
            self.schema_out.model_validate(item) for item in items_q.scalars().all()
        ]

    async def get(self, idx: int) -> Optional[schema_out]:
        """Get the item by id. If item not found - return None."""
        item = await self.__session.get(self.orm_model, idx)

        if not item:
            return None
        return self.schema_out.model_validate(item)

    async def update(self, item_id: int, data: schema_in) -> None:
        """Update the item by id. If item not found - raise ValueError."""
        data_dict = data.model_dump(exclude_unset=True)

        item = await self.__session.get(self.orm_model, item_id)
        if not item:
            raise ValueError(self.not_found_error_str)

        for key, value in data_dict.items():
            setattr(item, key, value)
        await self.__session.flush()

    async def delete(self, item_id: int) -> None:
        """Delete the item by id. If item not found - raise ValueError."""
        item = await self.__session.get(self.orm_model, item_id)
        if not item:
            raise ValueError(self.not_found_error_str)

        await self.__session.delete(item)
        await self.__session.commit()


class TaskRepository(BaseRepository):
    """The task repository."""

    orm_model: Type[Base] = Task
    schema_in: Type[BaseModel] = TaskInSchema
    schema_out: Type[BaseModel] = TaskOutSchema
    not_found_error_str: str = "The task not found"

    async def get_all_by_status(self, status: str) -> List[schema_out]:
        """Get all tasks with status (or all tasks if status is None)."""
        tasks_q = await self.__session.execute(
            select(Task).where(Task.status == status)
        )
        return [TaskOutSchema.model_validate(task) for task in tasks_q.scalars().all()]
