# app/repositories/password_reset_token/postgres.py

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.password_reset_token import PasswordResetToken


class PostgresPasswordResetTokenRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        token: PasswordResetToken,
    ) -> PasswordResetToken:

        self.db.add(token)
        self.db.flush()

        return token

    def get_by_hash(
        self,
        token_hash: str,
    ) -> PasswordResetToken | None:

        return (
            self.db.query(PasswordResetToken)
            .filter(PasswordResetToken.token_hash == token_hash)
            .first()
        )

    def mark_used(
        self,
        token: PasswordResetToken,
    ) -> PasswordResetToken:

        token.used_at = datetime.now(timezone.utc)

        self.db.flush()

        return token
