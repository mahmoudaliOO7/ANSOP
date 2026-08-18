"""Add allowlists and denylists tables.

Revision ID: 002
Revises: 001
Create Date: 2025-08-18 13:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add allowlists and denylists."""
    # Allowlists table
    op.create_table(
        'allowlist_entries',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('entry_type', sa.String(50), nullable=False),
        sa.Column('value', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_by_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ondelete='RESTRICT'),
    )
    op.create_index('ix_allowlist_entries_entry_type', 'allowlist_entries', ['entry_type'])
    op.create_index('ix_allowlist_entries_value', 'allowlist_entries', ['value'])

    # Denylists table
    op.create_table(
        'denylist_entries',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('entry_type', sa.String(50), nullable=False),
        sa.Column('value', sa.String(255), nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('expiry_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ondelete='RESTRICT'),
    )
    op.create_index('ix_denylist_entries_entry_type', 'denylist_entries', ['entry_type'])
    op.create_index('ix_denylist_entries_value', 'denylist_entries', ['value'])


def downgrade() -> None:
    """Downgrade to previous schema."""
    op.drop_index('ix_denylist_entries_value')
    op.drop_index('ix_denylist_entries_entry_type')
    op.drop_table('denylist_entries')
    
    op.drop_index('ix_allowlist_entries_value')
    op.drop_index('ix_allowlist_entries_entry_type')
    op.drop_table('allowlist_entries')
