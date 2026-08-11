"""convert roles to relational RBAC

Revision ID: ee2dd39b5b6d
Revises: c8188c444d98
Create Date: 2026-08-11 15:20:25.182796

"""

from alembic import op
import sqlalchemy as sa

revision = "ee2dd39b5b6d"
down_revision = "c8188c444d98"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # ---------------------------------------------------------
    # 1. Create roles table
    # ---------------------------------------------------------

    op.create_table(
        "roles",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),
        sa.Column(
            "name",
            sa.String(length=50),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "name",
            name="uq_roles_name",
        ),
    )

    # ---------------------------------------------------------
    # 2. Create permissions table
    # ---------------------------------------------------------

    op.create_table(
        "permissions",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),
        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "name",
            name="uq_permissions_name",
        ),
    )

    # ---------------------------------------------------------
    # 3. Create role_permissions junction table
    # ---------------------------------------------------------

    op.create_table(
        "role_permissions",
        sa.Column(
            "role_id",
            sa.Integer(),
            sa.ForeignKey(
                "roles.id",
                ondelete="CASCADE",
            ),
            primary_key=True,
        ),
        sa.Column(
            "permission_id",
            sa.Integer(),
            sa.ForeignKey(
                "permissions.id",
                ondelete="CASCADE",
            ),
            primary_key=True,
        ),
    )

    # ---------------------------------------------------------
    # 4. Insert initial roles
    # ---------------------------------------------------------

    roles_table = sa.table(
        "roles",
        sa.column("id", sa.Integer()),
        sa.column("name", sa.String()),
    )

    op.bulk_insert(
        roles_table,
        [
            {
                "id": 1,
                "name": "user",
            },
            {
                "id": 2,
                "name": "moderator",
            },
            {
                "id": 3,
                "name": "admin",
            },
        ],
    )

    # ---------------------------------------------------------
    # 5. Insert permissions
    # ---------------------------------------------------------

    permissions_table = sa.table(
        "permissions",
        sa.column("id", sa.Integer()),
        sa.column("name", sa.String()),
    )

    op.bulk_insert(
        permissions_table,
        [
            {"id": 1, "name": "users:view"},
            {"id": 2, "name": "users:update"},
            {"id": 3, "name": "users:delete"},
            {"id": 4, "name": "users:change_role"},
            {"id": 5, "name": "users:ban"},
            {"id": 6, "name": "profile:view"},
            {"id": 7, "name": "profile:update"},
            {"id": 8, "name": "orders:view"},
            {"id": 9, "name": "orders:create"},
            {"id": 10, "name": "orders:refund"},
            {"id": 11, "name": "games:view"},
            {"id": 12, "name": "games:create"},
            {"id": 13, "name": "games:start"},
            {"id": 14, "name": "games:moderate"},
        ],
    )

    # ---------------------------------------------------------
    # 6. Assign permissions to roles
    # ---------------------------------------------------------

    role_permissions_table = sa.table(
        "role_permissions",
        sa.column("role_id", sa.Integer()),
        sa.column("permission_id", sa.Integer()),
    )

    op.bulk_insert(
        role_permissions_table,
        [
            # USER
            {"role_id": 1, "permission_id": 6},  # profile:view
            {"role_id": 1, "permission_id": 7},  # profile:update
            {"role_id": 1, "permission_id": 8},  # orders:view
            # MODERATOR
            {"role_id": 2, "permission_id": 1},  # users:view
            {"role_id": 2, "permission_id": 5},  # users:ban
            {"role_id": 2, "permission_id": 14},  # games:moderate
            # ADMIN
            {"role_id": 3, "permission_id": 1},  # users:view
            {"role_id": 3, "permission_id": 2},  # users:update
            {"role_id": 3, "permission_id": 3},  # users:delete
            {"role_id": 3, "permission_id": 4},  # users:change_role
            {"role_id": 3, "permission_id": 5},  # users:ban
            {"role_id": 3, "permission_id": 8},  # orders:view
            {"role_id": 3, "permission_id": 9},  # orders:create
            {"role_id": 3, "permission_id": 10},  # orders:refund
            {"role_id": 3, "permission_id": 11},  # games:view
            {"role_id": 3, "permission_id": 12},  # games:create
            {"role_id": 3, "permission_id": 13},  # games:start
            {"role_id": 3, "permission_id": 14},  # games:moderate
        ],
    )

    # ---------------------------------------------------------
    # 7. Add role_id to existing users
    # ---------------------------------------------------------

    op.add_column(
        "users",
        sa.Column(
            "role_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # ---------------------------------------------------------
    # 8. Convert existing role values into role_id
    # ---------------------------------------------------------

    op.execute("""
        UPDATE users
        SET role_id = roles.id
        FROM roles
        WHERE users.role::text = roles.name
    """)

    # ---------------------------------------------------------
    # 9. Make role_id mandatory
    # ---------------------------------------------------------

    op.alter_column(
        "users",
        "role_id",
        nullable=False,
    )

    # ---------------------------------------------------------
    # 10. Add foreign key
    # ---------------------------------------------------------

    op.create_foreign_key(
        "fk_users_role_id_roles",
        "users",
        "roles",
        ["role_id"],
        ["id"],
    )

    # ---------------------------------------------------------
    # 11. Remove old ENUM role column
    # ---------------------------------------------------------

    op.drop_column(
        "users",
        "role",
    )

    # ---------------------------------------------------------
    # 12. Remove old PostgreSQL ENUM type
    # ---------------------------------------------------------

    op.execute("DROP TYPE IF EXISTS userrole")


def downgrade() -> None:

    # Recreate old ENUM
    op.execute("""
        CREATE TYPE userrole AS ENUM (
            'user',
            'moderator',
            'admin'
        )
        """)

    # Add old role column back
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.Enum(
                "user",
                "moderator",
                "admin",
                name="userrole",
            ),
            nullable=True,
        ),
    )

    # Convert role_id back to role
    op.execute("""
        UPDATE users
        SET role = roles.name
        FROM roles
        WHERE users.role_id = roles.id
        """)

    op.alter_column(
        "users",
        "role",
        nullable=False,
    )

    # Remove FK
    op.drop_constraint(
        "fk_users_role_id_roles",
        "users",
        type_="foreignkey",
    )

    # Remove role_id
    op.drop_column(
        "users",
        "role_id",
    )

    # Remove RBAC tables
    op.drop_table("role_permissions")
    op.drop_table("permissions")
    op.drop_table("roles")

    # Remove enum
    op.execute("DROP TYPE IF EXISTS userrole")
