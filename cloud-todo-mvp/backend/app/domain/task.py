from dataclasses import dataclass
from datetime import date, datetime

from app.domain.enums import TaskPriority, TaskStatus


@dataclass(slots=True)
class Task:
    id: str
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_date: date | None
    created_at: datetime
    updated_at: datetime
