from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import decode_access_token, oauth2_scheme
from app.db.database import get_db
from app.db.unit_of_work import UnitOfWork
from app.models.user import User
from app.repositories.refresh_token.postgres import PostgresRefreshTokenRepository
from app.repositories.role.interface import IRoleRepository
from app.repositories.role.postgres import PostgresRoleRepository
from app.repositories.user.interface import IUserRepository
from app.repositories.user.postgres import PostgresUserRepository
from app.services.auth_service import AuthService
from app.repositories.refresh_token.interface import IRefreshTokenRepository
from app.services.user_service import UserService


def get_user_repository(
    db: Session = Depends(get_db),
) -> IUserRepository:
    return PostgresUserRepository(db)


def get_role_repository(
    db: Session = Depends(get_db),
) -> IRoleRepository:
    return PostgresRoleRepository(db)


def get_refresh_token_repository(
    db: Session = Depends(get_db),
) -> IRefreshTokenRepository:

    return PostgresRefreshTokenRepository(db)


def get_unit_of_work(
    db: Session = Depends(get_db),
) -> UnitOfWork:

    return UnitOfWork(db)


def get_auth_service(
    user_repository: IUserRepository = Depends(get_user_repository),
    role_repository: IRoleRepository = Depends(get_role_repository),
    refresh_token_repository: IRefreshTokenRepository = Depends(
        get_refresh_token_repository
    ),
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> AuthService:

    return AuthService(
        user_repository=user_repository,
        role_repository=role_repository,
        refresh_token_repository=refresh_token_repository,
        unit_of_work=unit_of_work,
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    repository: IUserRepository = Depends(get_user_repository),
) -> User:

    payload = decode_access_token(token)

    user_id = int(payload["sub"])

    user = repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_user_service(
    repository: IUserRepository = Depends(get_user_repository),
    role_repository: IRoleRepository = Depends(get_role_repository),
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    refresh_token_repository: IRefreshTokenRepository = Depends(
        get_refresh_token_repository
    ),
) -> UserService:

    return UserService(
        user_repository=repository,
        role_repository=role_repository,
        unit_of_work=unit_of_work,
        refresh_token_repository=refresh_token_repository,
    )


def require_permission(permission_name: str):

    def permission_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        permissions = current_user.role.permissions

        has_permission = any(
            permission.name == permission_name for permission in permissions
        )

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return permission_checker
