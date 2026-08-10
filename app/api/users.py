from fastapi import APIRouter, Depends

from app.api.authorization import require_role
from app.api.dependencies import get_user_service
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.auth import UserResponse
from app.schemas.user import UpdateUserRoleRequest
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.patch(
    "/{user_id}/role",
    response_model=UserResponse,
)
def update_user_role(
    user_id: int,
    request: UpdateUserRoleRequest,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.update_role(
        user_id=user_id,
        role=request.role,
    )
