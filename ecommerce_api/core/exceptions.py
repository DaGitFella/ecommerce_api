from dataclasses import dataclass, field
from http import HTTPStatus


@dataclass
class AppError(Exception):
    message: str
    status_code: int = field(default=HTTPStatus.INTERNAL_SERVER_ERROR.value)
    detail: str | None = None

    def __str__(self) -> str:
        return self.message


class ConflictError(AppError):
    def __init__(self, message: str, detail: str | None = None) -> None:
        super().__init__(
            message=message, status_code=HTTPStatus.CONFLICT.value, detail=detail
        )
