"""add note to unit email recipients

Revision ID: e7f2a3ab9b6c
Revises: a1f4d9b0c7aa
Create Date: 2025-09-13 20:50:40.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7f2a3ab9b6c'
down_revision: Union[str, None] = 'a1f4d9b0c7aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('unit_email_recipients', sa.Column('note', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('unit_email_recipients', 'note')
