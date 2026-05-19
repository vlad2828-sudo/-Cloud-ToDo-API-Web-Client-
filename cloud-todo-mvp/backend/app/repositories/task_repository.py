from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.db.models import TaskModel
from app.domain.enums import TaskPriority, TaskStatus


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, task: TaskModel) -> TaskModel:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: str) -> TaskModel | None:
        return self.db.get(TaskModel, task_id)

    def list(
        self,
        *,
        status: TaskStatus | None,
        priority: TaskPriority | None,
        limit: int,
        offset: int,
    ) -> tuple[list[TaskModel], int]:
        base_query = select(TaskModel)
        base_query = self._apply_filters(base_query, status=status, priority=priority)

        total_query = select(func.count()).select_from(TaskModel)
        total_query = self._apply_filters(total_query, status=status, priority=priority)
        total = self.db.scalar(total_query) or 0

        rows = self.db.scalars(
            base_query.order_by(TaskModel.created_at.desc()).limit(limit).offset(offset)
        ).all()
        return list(rows), total

    def update(self, task: TaskModel) -> TaskModel:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: TaskModel) -> None:
        self.db.delete(task)
        self.db.commit()

    @staticmethod
    def _apply_filters(
        query: Select,
        *,
        status: TaskStatus | None,
        priority: TaskPriority | None,
    ) -> Select:
        if status is not None:
            query = query.where(TaskModel.status == status)
        if priority is not None:
            query = query.where(TaskModel.priority == priority)
        return query
