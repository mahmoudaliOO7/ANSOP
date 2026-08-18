"""Initial schema creation.

Revision ID: 001
Revises: None
Create Date: 2025-08-18 13:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create ENUM types
    op.execute(
        'CREATE TYPE role_enum AS ENUM (\"ADMIN\", \"SOC_ANALYST\", \"APPROVER\", \"VIEWER\")'
    )
    op.execute(
        'CREATE TYPE severity_enum AS ENUM (\"CRITICAL\", \"HIGH\", \"MEDIUM\", \"LOW\", \"INFO\")'
    )
    op.execute(
        'CREATE TYPE detection_status_enum AS ENUM (\"NEW\", \"ACKNOWLEDGED\", \"RESOLVED\", \"CLOSED\")'
    )
    op.execute(
        'CREATE TYPE incident_status_enum AS ENUM (\"NEW\", \"TRIAGED\", \"INVESTIGATING\", \"CONTAINMENT\", \"RESOLVED\", \"CLOSED\")'
    )
    op.execute(
        'CREATE TYPE approval_status_enum AS ENUM (\"PENDING_APPROVAL\", \"APPROVED\", \"REJECTED\", \"EXPIRED\", \"EXECUTED\", \"SUCCESS\", \"FAILED\")'
    )
    op.execute(
        'CREATE TYPE response_status_enum AS ENUM (\"PENDING\", \"EXECUTING\", \"SUCCESS\", \"FAILED\", \"ROLLED_BACK\")'
    )
    op.execute(
        'CREATE TYPE device_type_enum AS ENUM (\"FIREWALL\", \"ROUTER\", \"IDS\", \"IDS_IPS\", \"SWITCH\", \"PROXY\", \"SIMULATOR\")'
    )
    op.execute(
        'CREATE TYPE audit_action_enum AS ENUM (\"LOGIN\", \"LOGOUT\", \"CREATE\", \"UPDATE\", \"DELETE\", \"APPROVE\", \"REJECT\", \"EXECUTE\", \"ENRICH\", \"RISK_ASSESS\")'
    )

    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column("username", sa.String(255), nullable=False, unique=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("full_name", sa.String(255), nullable=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("is_superuser", sa.Boolean(), default=False, nullable=False),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_username", "users", ["username"])
    op.create_index("ix_users_email", "users", ["email"])

    # Create roles table
    op.create_table(
        "roles",
        sa.Column("id", sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("description", sa.String(1000), nullable=True),
        sa.Column("created_at", sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_roles_name", "roles", ["name"])

    # Create permissions table
    op.create_table(
        "permissions",
        sa.Column("id", sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("description", sa.String(1000), nullable=True),
        sa.Column("resource", sa.String(255), nullable=False),
        sa.Column("action", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_permissions_resource_action", "permissions", ["resource", "action"])

    # Create user_roles table
    op.create_table(
        "user_roles",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("role_id", sa.UUID(), nullable=False),
        sa.Column("assigned_at", sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "role_id"),
    )

    # Create role_permissions table
    op.create_table(
        "role_permissions",
        sa.Column("role_id", sa.UUID(), nullable=False),
        sa.Column("permission_id", sa.UUID(), nullable=False),
        sa.Column("assigned_at", sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["permission_id"], ["permissions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("role_id", "permission_id"),
    )


def downgrade() -> None:
    op.drop_table("role_permissions")
    op.drop_table("user_roles")
    op.drop_table("permissions")
    op.drop_table("roles")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS audit_action_enum")
    op.execute("DROP TYPE IF EXISTS device_type_enum")
    op.execute("DROP TYPE IF EXISTS response_status_enum")
    op.execute("DROP TYPE IF EXISTS approval_status_enum")
    op.execute("DROP TYPE IF EXISTS incident_status_enum")
    op.execute("DROP TYPE IF EXISTS detection_status_enum")
    op.execute("DROP TYPE IF EXISTS severity_enum")
    op.execute("DROP TYPE IF EXISTS role_enum")
