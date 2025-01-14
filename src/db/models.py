"""The module responsible for model descriptions in the database."""

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base orm class."""

    pass


class Task(Base):
    """ORM representation of a table in which task records will be stored."""

    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(15), nullable=False)

    def __repr__(self) -> str:
        """Return the string representation of the object."""
        return f"{self.title} ({self.id}), status: {self.status}"
