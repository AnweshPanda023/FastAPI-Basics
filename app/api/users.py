from fastapi import APIRouter, Depends
from starlette import status

from app.api.dependencies import (
    get_current_user,
    get_user_service,
)
from app.models.user import User
from app.schemas.auth import ChangePasswordRequest
from app.schemas.user import (
    ChangePasswordResponse,
    UpdateProfileRequest,
    UserResponse,
)
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.patch(
    "/me",
    response_model=UserResponse,
)
def update_me(
    request: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.update_profile(
        user_id=current_user.id,
        email=request.email,
        full_name=request.full_name,
    )


@router.post(
    "/me/change-password",
    response_model=ChangePasswordResponse,
    status_code=status.HTTP_200_OK,
)
def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    user_service.change_password(
        user=current_user,
        current_password=request.current_password,
        new_password=request.new_password,
    )

    return ChangePasswordResponse(message="Password changed successfully")
