"""sample

Revision ID: 2d9e9fdefa2b
Revises: 389b60d3f9d0
Create Date: 2025-04-15 17:07:30.592139

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d9e9fdefa2b'
down_revision: Union[str, None] = '389b60d3f9d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'samples',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('order_id', sa.Integer, nullable=False),
        sa.Column('particulars', sa.String(255), nullable=True),
        sa.Column('quantity', sa.Float, nullable=True),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('condition', sa.String(255), nullable=True),
        sa.Column('sample_type', sa.String(100), nullable=True),
        sa.Column('collect_date', sa.Date, nullable=True),
        sa.Column('receipt_date', sa.Date, nullable=True),
        sa.Column('collected_by', sa.String(255), nullable=True),
        sa.Column('is_delete', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

def downgrade() -> None:
    op.drop_table('samples')