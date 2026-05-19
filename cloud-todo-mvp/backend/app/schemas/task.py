from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.enums import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    status: TaskStatus = TaskStatus.NEW
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: date | None = Field(default=None, alias="dueDate")

    model_config = ConfigDict(populate_by_name=True)


class TaskPutUpdate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    status: TaskStatus
    priority: TaskPriority
    due_date: date | None = Field(default=None, alias="dueDate")

    model_config = ConfigDict(populate_by_name=True)


class TaskPatchUpdate(BaseModel):
    status: TaskStatus | None = None
    priority: TaskPriority | None = None

    @model_validator(mode="after")
    def require_at_least_one_field(self) -> "TaskPatchUpdate":
        if self.status is None and self.priority is None:
            raise ValueError("At least one of status or priority must be provided")
        return self


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_date: date | None = Field(alias="dueDate")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    total: int
    limit: int
    offset: int
