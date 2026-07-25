from typing import Protocol

from app.models.refresh_token import RefreshToken


class IRefreshTokenRepository(Protocol):

    def create(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        ...

    def get_by_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        ...

    def revoke(
        self,
        refresh_token: RefreshToken,
    ) -> None:
        ...

    def revoke_all_for_user(
        self,
        user_id: int,
    ) -> None:
        ...