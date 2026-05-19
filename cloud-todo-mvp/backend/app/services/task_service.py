import uuid

from app.core.errors import TaskNotFoundError
from app.db.models import TaskModel
from app.domain.enums import TaskPriority, TaskStatus
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskPatchUpdate, TaskPutUpdate


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def create_task(self, payload: TaskCreate) -> TaskModel:
        task = TaskModel(
            id=str(uuid.uuid4()),
            title=payload.title,
            description=payload.description,
            status=payload.status,
            priority=payload.priority,
            due_date=payload.due_date,
        )
        return self.repository.create(task)

    def list_tasks(
        self,
        *,
        status: TaskStatus | None,
        priority: TaskPriority | None,
        limit: int,
        offset: int,
    ) -> tuple[list[TaskModel], int]:
        return self.repository.list(status=status, priority=priority, limit=limit, offset=offset)

    def get_task(self, task_id: str) -> TaskModel:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def replace_task(self, task_id: str, payload: TaskPutUpdate) -> TaskModel:
        task = self.get_task(task_id)
        task.title = payload.title
        task.description = payload.description
        task.status = payload.status
        task.priority = payload.priority
        task.due_date = payload.due_date
        return self.repository.update(task)

    def patch_task(self, task_id: str, payload: TaskPatchUpdate) -> TaskModel:
        task = self.get_task(task_id)
        if payload.status is not None:
            task.status = payload.status
        if payload.priority is not None:
            task.priority = payload.priority
        return self.repository.update(task)

    def delete_task(self, task_id: str) -> None:
        task = self.get_task(task_id)
        self.repository.delete(task)
