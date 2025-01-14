"""The module responsible for database queries."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.schemas import TaskInSchema, TaskOutSchema

from .models import Task


class BaseRepository(object):
    """
    Base repository.

    Args:
        session (AsyncSession) - async session object.
    """

    not_found_error_str: str = "Item not found"

    def __init__(self, session: AsyncSession):
        """Initialize class."""
        self.session = session


class TaskRepository(BaseRepository):
    """The task repository."""

    not_found_error_str: str = "The task not found"

    async def create(self, data: TaskInSchema) -> int:
        """Create a new item."""
        new_item = Task(**data.model_dump())
        self.session.add(new_item)
        await self.session.commit()
        return new_item.id

    async def get_all(self) -> List[TaskOutSchema]:
        """Get all items."""
        items_q = await self.session.execute(select(Task))
        return [TaskOutSchema.model_validate(item) for item in items_q.scalars().all()]

    async def get(self, idx: int) -> Optional[TaskOutSchema]:
        """Get the item by id. If item not found - return None."""
        item = await self.session.get(Task, idx)

        if not item:
            return None
        return TaskOutSchema.model_validate(item)

    async def update(self, item_id: int, data: TaskInSchema) -> None:
        """Update the item by id. If item not found - raise ValueError."""
        data_dict = data.model_dump(exclude_unset=True)

        item = await self.session.get(Task, item_id)
        if not item:
            raise ValueError(self.not_found_error_str)

        for key, value in data_dict.items():
            setattr(item, key, value)
        await self.session.flush()

    async def delete(self, item_id: int) -> None:
        """Delete the item by id. If item not found - raise ValueError."""
        item = await self.session.get(Task, item_id)
        if not item:
            raise ValueError(self.not_found_error_str)

        await self.session.delete(item)
        await self.session.commit()

    async def get_all_by_status(self, status: str) -> List[TaskOutSchema]:
        """Get all tasks with status (or all tasks if status is None)."""
        tasks_q = await self.session.execute(select(Task).where(Task.status == status))
        return [TaskOutSchema.model_validate(task) for task in tasks_q.scalars().all()]
