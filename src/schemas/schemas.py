from typing import Any
from typing_extensions import Self

from pydantic import BaseModel, field_validator

STATUSES = {
    "todo",
    "in_progress",
    "done",
}


class TaskIn(BaseModel):
    title: str
    description: str
    status: str

    @classmethod
    @field_validator("status")
    def validate_status(cls, status: Any) -> str:
        if status not in STATUSES:
            raise ValueError(f"Status must be in {str(STATUSES)}")
        return status
