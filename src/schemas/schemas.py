from typing import Any

from pydantic import BaseModel, field_validator

STATUSES = {
    "todo",
    "in_progress",
    "done",
}


class Task(BaseModel):
    title: str
    description: str
    status: str


class TaskIn(Task):

    @classmethod
    @field_validator("status")
    def validate_status(cls, status: Any) -> str:
        if status not in STATUSES:
            raise ValueError(f"Status must be in {str(STATUSES)}")
        return status


class TaskOut(Task):
    id: int
