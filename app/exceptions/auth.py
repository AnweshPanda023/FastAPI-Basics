from starlette import status

from app.exceptions.base import AppException


class InvalidCredentialsException(AppException):

    def __init__(
        self,
        message: str = "Invalid email or password",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTH_INVALID_CREDENTIALS",
        )


class EmailAlreadyExistsException(AppException):

    def __init__(
        self,
        message: str = "Email already registered",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="AUTH_EMAIL_ALREADY_EXISTS",
        )


class InvalidRefreshTokenException(AppException):

    def __init__(
        self,
        message: str = "Invalid refresh token",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTH_INVALID_REFRESH_TOKEN",
        )


class RefreshTokenExpiredException(AppException):

    def __init__(
        self,
        message: str = "Refresh token expired",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTH_REFRESH_TOKEN_EXPIRED",
        )


class UserNotFoundException(AppException):

    def __init__(
        self,
        message: str = "User not found",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="AUTH_USER_NOT_FOUND",
        )


class RoleNotFoundException(AppException):

    def __init__(
        self,
        message: str = "Role not found",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="AUTH_ROLE_NOT_FOUND",
        )


class InvalidCurrentPasswordException(AppException):

    def __init__(self):
        super().__init__(
            message="Current password is incorrect",
            status_code=400,
            error_code="INVALID_CURRENT_PASSWORD",
        )


class SamePasswordException(AppException):

    def __init__(self):
        super().__init__(
            message="Current password is same as existing one",
            status_code=400,
            error_code="SAME_CURRENT_PASSWORD",
        )
