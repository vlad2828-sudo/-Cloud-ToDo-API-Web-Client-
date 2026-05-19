from fastapi import Header, status

from app.core.config import settings
from app.core.errors import AppError


def require_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    if not x_api_key or x_api_key != settings.api_key:
        raise AppError(
            code="UNAUTHORIZED",
            message="Invalid or missing API key",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
