"""add performance indexes

Revision ID: 52bb508b1c90
Revises: 206c64dbf029
Create Date: 2025-09-13 15:33:09.773420

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52bb508b1c90'
down_revision: Union[str, None] = '206c64dbf029'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # persons
    op.create_index('ix_persons_full_name', 'persons', ['full_name'], unique=False)
    op.create_index('ix_persons_unit', 'persons', ['unit_id'], unique=False)
    op.create_index('ix_persons_position', 'persons', ['position_id'], unique=False)
    # work_processes
    op.create_index('ix_work_person', 'work_processes', ['person_id'], unique=False)
    # salary_histories
    op.create_index('ix_salary_person', 'salary_histories', ['person_id'], unique=False)
    # insurance_events
    op.create_index('ix_insurance_person', 'insurance_events', ['person_id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_insurance_person', table_name='insurance_events')
    op.drop_index('ix_salary_person', table_name='salary_histories')
    op.drop_index('ix_work_person', table_name='work_processes')
    op.drop_index('ix_persons_position', table_name='persons')
    op.drop_index('ix_persons_unit', table_name='persons')
    op.drop_index('ix_persons_full_name', table_name='persons')
