from starlette import status

from app.exceptions.base import AppException


class InsufficientPermissionsException(AppException):

    def __init__(
        self,
        message: str = "Insufficient permissions",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="AUTH_INSUFFICIENT_PERMISSIONS",
        )
