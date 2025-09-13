"""add unit email recipients table

Revision ID: a1f4d9b0c7aa
Revises: dbc80bed28f1
Create Date: 2025-09-13 20:23:40.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1f4d9b0c7aa'
down_revision: Union[str, None] = 'dbc80bed28f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'unit_email_recipients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('unit_id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['unit_id'], ['units.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('unit_id', 'email', name='uq_unit_email'),
    )


def downgrade() -> None:
    op.drop_table('unit_email_recipients')
