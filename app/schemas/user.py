from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class RoleResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True,
    }


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    role: RoleResponse
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class UpdateUserRoleRequest(BaseModel):
    role: str


class PaginatedUsersResponse(BaseModel):
    items: list[UserResponse]
    page: int
    page_size: int
    total: int
    total_pages: int


class UserListParams(BaseModel):
    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
    )

    search: str | None = None

    role: str | None = None

    is_active: bool | None = None

class UpdateProfileRequest(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
