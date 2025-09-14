"""add composite index for unit_email_recipients and helpful indexes for email_logs

Revision ID: f1a2b3c4d5e6
Revises: e7f2a3ab9b6c
Create Date: 2025-09-14 07:08:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f1a2b3c4d5e6'
down_revision: Union[str, None] = 'e7f2a3ab9b6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # unit_email_recipients: composite index to speed queries by unit and active
    try:
        op.create_index('ix_unit_email_recipients_unit_active', 'unit_email_recipients', ['unit_id', 'active'], unique=False)
    except Exception:
        pass
    # email_logs: helpful indexes for common filters
    try:
        op.create_index('ix_email_logs_created_at', 'email_logs', ['created_at'], unique=False)
    except Exception:
        pass
    try:
        op.create_index('ix_email_logs_type', 'email_logs', ['type'], unique=False)
    except Exception:
        pass
    try:
        op.create_index('ix_email_logs_status', 'email_logs', ['status'], unique=False)
    except Exception:
        pass
    try:
        op.create_index('ix_email_logs_unit_name', 'email_logs', ['unit_name'], unique=False)
    except Exception:
        pass


def downgrade() -> None:
    try:
        op.drop_index('ix_email_logs_unit_name', table_name='email_logs')
    except Exception:
        pass
    try:
        op.drop_index('ix_email_logs_status', table_name='email_logs')
    except Exception:
        pass
    try:
        op.drop_index('ix_email_logs_type', table_name='email_logs')
    except Exception:
        pass
    try:
        op.drop_index('ix_email_logs_created_at', table_name='email_logs')
    except Exception:
        pass
    try:
        op.drop_index('ix_unit_email_recipients_unit_active', table_name='unit_email_recipients')
    except Exception:
        pass
