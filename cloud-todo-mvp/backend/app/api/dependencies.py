from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


def get_task_service(db: Session = Depends(get_db)) -> Generator[TaskService, None, None]:
    yield TaskService(TaskRepository(db))
