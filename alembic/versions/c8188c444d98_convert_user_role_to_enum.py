"""convert user role to enum

Revision ID: c8188c444d98
Revises: f1782479d02c
Create Date: 2026-08-11

"""

from alembic import op
import sqlalchemy as sa

revision = "c8188c444d98"
down_revision = "f1782479d02c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    userrole = sa.Enum(
        "user",
        "moderator",
        "admin",
        name="userrole",
    )

    userrole.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.alter_column(
        "users",
        "role",
        existing_type=sa.VARCHAR(length=50),
        type_=userrole,
        postgresql_using="role::text::userrole",
        existing_nullable=False,
    )


def downgrade() -> None:
    userrole = sa.Enum(
        "user",
        "moderator",
        "admin",
        name="userrole",
    )

    op.alter_column(
        "users",
        "role",
        existing_type=userrole,
        type_=sa.VARCHAR(length=50),
        postgresql_using="role::text",
        existing_nullable=False,
    )

    userrole.drop(
        op.get_bind(),
        checkfirst=True,
    )
