from datetime import date, datetime, timezone

import pytest

from app.core.errors import TaskNotFoundError
from app.db.models import TaskModel
from app.domain.enums import TaskPriority, TaskStatus
from app.schemas.task import TaskCreate, TaskPatchUpdate, TaskPutUpdate
from app.services.task_service import TaskService


class FakeTaskRepository:
    def __init__(self) -> None:
        self.items: dict[str, TaskModel] = {}
        self.deleted_ids: list[str] = []

    def create(self, task: TaskModel) -> TaskModel:
        now = datetime.now(timezone.utc)
        task.created_at = now
        task.updated_at = now
        self.items[task.id] = task
        return task

    def get_by_id(self, task_id: str) -> TaskModel | None:
        return self.items.get(task_id)

    def list(self, *, status, priority, limit, offset):
        rows = list(self.items.values())
        if status is not None:
            rows = [task for task in rows if task.status == status]
        if priority is not None:
            rows = [task for task in rows if task.priority == priority]
        return rows[offset : offset + limit], len(rows)

    def update(self, task: TaskModel) -> TaskModel:
        task.updated_at = datetime.now(timezone.utc)
        self.items[task.id] = task
        return task

    def delete(self, task: TaskModel) -> None:
        self.deleted_ids.append(task.id)
        self.items.pop(task.id, None)


def make_service() -> tuple[TaskService, FakeTaskRepository]:
    repo = FakeTaskRepository()
    return TaskService(repo), repo


def test_create_task_sets_defaults() -> None:
    service, _ = make_service()

    task = service.create_task(TaskCreate(title="Buy milk"))

    assert task.id
    assert task.status == TaskStatus.NEW
    assert task.priority == TaskPriority.MEDIUM


def test_create_task_accepts_due_date() -> None:
    service, _ = make_service()

    task = service.create_task(TaskCreate(title="Submit report", dueDate=date(2026, 5, 1)))

    assert task.due_date == date(2026, 5, 1)


def test_get_task_raises_not_found() -> None:
    service, _ = make_service()

    with pytest.raises(TaskNotFoundError):
        service.get_task("missing-id")


def test_replace_task_updates_all_fields() -> None:
    service, _ = make_service()
    task = service.create_task(TaskCreate(title="Old title"))

    updated = service.replace_task(
        task.id,
        TaskPutUpdate(
            title="New title",
            description="New description",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            dueDate=date(2026, 6, 1),
        ),
    )

    assert updated.title == "New title"
    assert updated.description == "New description"
    assert updated.status == TaskStatus.IN_PROGRESS
    assert updated.priority == TaskPriority.HIGH
    assert updated.due_date == date(2026, 6, 1)


def test_patch_task_updates_status_and_priority() -> None:
    service, _ = make_service()
    task = service.create_task(TaskCreate(title="Patch me"))

    updated = service.patch_task(
        task.id,
        TaskPatchUpdate(status=TaskStatus.DONE, priority=TaskPriority.LOW),
    )

    assert updated.status == TaskStatus.DONE
    assert updated.priority == TaskPriority.LOW


def test_delete_task_removes_item() -> None:
    service, repo = make_service()
    task = service.create_task(TaskCreate(title="Delete me"))

    service.delete_task(task.id)

    assert task.id in repo.deleted_ids
    assert repo.get_by_id(task.id) is None
