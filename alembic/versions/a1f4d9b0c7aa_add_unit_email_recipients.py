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
    """
    Tạo bảng nếu chưa tồn tại. Nếu đã tồn tại (do khởi tạo thủ công trước đó),
    đảm bảo các cột/unique constraint cần thiết đã có để bảo toàn logic ứng dụng.
    """
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    tables = set(inspector.get_table_names())
    if 'unit_email_recipients' in tables:
        # Đảm bảo các cột bắt buộc tồn tại
        try:
            cols = {c['name'] for c in inspector.get_columns('unit_email_recipients')}
        except Exception:
            cols = set()
        if 'active' not in cols:
            try:
                op.add_column('unit_email_recipients', sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.text('1')))
            except Exception:
                pass
        if 'created_at' not in cols:
            try:
                op.add_column('unit_email_recipients', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))
            except Exception:
                pass
        # Đảm bảo unique constraint (unit_id, email)
        try:
            uqs = [uc.get('name') for uc in inspector.get_unique_constraints('unit_email_recipients')]
            if 'uq_unit_email' not in set(uqs):
                op.create_unique_constraint('uq_unit_email', 'unit_email_recipients', ['unit_id', 'email'])
        except Exception:
            pass
        return

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
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    try:
        if 'unit_email_recipients' in set(inspector.get_table_names()):
            op.drop_table('unit_email_recipients')
    except Exception:
        # Bỏ qua nếu đã bị xóa/không tồn tại
        pass
