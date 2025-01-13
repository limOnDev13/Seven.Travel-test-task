from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator

STATUSES = {
    "todo",
    "in_progress",
    "done",
}


class TaskSchema(BaseModel):
    title: str
    description: str
    status: str


class TaskInSchema(TaskSchema):

    @classmethod
    @field_validator("status")
    def validate_status(cls, status: Any) -> str:
        if status not in STATUSES:
            raise ValueError(f"Status must be in {str(STATUSES)}")
        return status


class TaskOutSchema(TaskSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
