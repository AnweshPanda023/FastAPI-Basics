# app/repositories/password_reset_token/interface.py

from typing import Protocol

from app.models.password_reset_token import PasswordResetToken


class IPasswordResetTokenRepository(Protocol):

    def create(
        self,
        token: PasswordResetToken,
    ) -> PasswordResetToken: ...

    def get_by_hash(
        self,
        token_hash: str,
    ) -> PasswordResetToken | None: ...

    def mark_used(
        self,
        token: PasswordResetToken,
    ) -> PasswordResetToken: ...
