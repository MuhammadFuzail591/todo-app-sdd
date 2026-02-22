from dataclasses import dataclass, field
from enum import Enum


class Status(Enum):
    """Completion state of a todo."""

    PENDING = "pending"
    COMPLETED = "completed"


@dataclass
class Todo:
    """Represents a single task."""

    id: int
    title: str
    status: Status = field(default=Status.PENDING)
