"""The module responsible for pydantic schemes."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

STATUSES = {
    "todo",
    "in_progress",
    "done",
}


class TaskSchema(BaseModel):
    """Base task schema."""

    title: str = Field(
        ...,
        description="Task title",
    )
    description: str = Field(
        ...,
        description="Task description",
    )
    status: str = Field(
        ..., description=f"The status of the task. It can only take values: {STATUSES}"
    )


class TaskInSchema(TaskSchema):
    """The task schema that comes from the client."""

    @field_validator("status")
    def validate_status(cls, status: Any) -> str:
        """Validate the field status - must be in STATUSES."""
        if status not in STATUSES:
            raise ValueError(f"Status must be in {STATUSES}")
        return status


class TaskOutSchema(TaskSchema):
    """The schema of the task that the server returns."""

    model_config = ConfigDict(from_attributes=True)
    id: int
