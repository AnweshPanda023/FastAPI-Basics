from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token.interface import (
    IRefreshTokenRepository,
)


class PostgresRefreshTokenRepository(IRefreshTokenRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:

        self.db.add(refresh_token)

        return refresh_token

    def get_active_tokens_by_user_id(
        self,
        user_id: int,
    ) -> list[RefreshToken]:

        return (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
                RefreshToken.expires_at > datetime.now(timezone.utc),
            )
            .all()
        )

    def revoke(
        self,
        refresh_token: RefreshToken,
    ) -> None:

        refresh_token.revoked_at = datetime.now(timezone.utc)

    def get_by_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:

        return (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked_at.is_(None),
            )
            .first()
        )