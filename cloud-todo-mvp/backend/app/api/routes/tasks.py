from fastapi import APIRouter, Depends, Query, Response, status

from app.api.dependencies import get_task_service
from app.core.security import require_api_key
from app.domain.enums import TaskPriority, TaskStatus
from app.schemas.error import ErrorResponse
from app.schemas.task import TaskCreate, TaskListResponse, TaskPatchUpdate, TaskPutUpdate, TaskResponse
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

ERROR_RESPONSES = {
    400: {"model": ErrorResponse},
    401: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    409: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
}


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
    dependencies=[Depends(require_api_key)],
)
def create_task(payload: TaskCreate, service: TaskService = Depends(get_task_service)) -> TaskResponse:
    return TaskResponse.model_validate(service.create_task(payload))


@router.get("", response_model=TaskListResponse, responses=ERROR_RESPONSES)
def list_tasks(
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    priority: TaskPriority | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: TaskService = Depends(get_task_service),
) -> TaskListResponse:
    items, total = service.list_tasks(status=status_filter, priority=priority, limit=limit, offset=offset)
    return TaskListResponse(
        items=[TaskResponse.model_validate(item) for item in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{task_id}", response_model=TaskResponse, responses=ERROR_RESPONSES)
def get_task(task_id: str, service: TaskService = Depends(get_task_service)) -> TaskResponse:
    return TaskResponse.model_validate(service.get_task(task_id))


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    responses=ERROR_RESPONSES,
    dependencies=[Depends(require_api_key)],
)
def replace_task(
    task_id: str,
    payload: TaskPutUpdate,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    return TaskResponse.model_validate(service.replace_task(task_id, payload))


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    responses=ERROR_RESPONSES,
    dependencies=[Depends(require_api_key)],
)
def patch_task(
    task_id: str,
    payload: TaskPatchUpdate,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    return TaskResponse.model_validate(service.patch_task(task_id, payload))


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=ERROR_RESPONSES,
    dependencies=[Depends(require_api_key)],
)
def delete_task(task_id: str, service: TaskService = Depends(get_task_service)) -> Response:
    service.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
