from pydantic import BaseModel

from app.models.enums import UserRole


class UpdateUserRoleRequest(BaseModel):
    role: UserRole
