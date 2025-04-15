"""perameter

Revision ID: 2e50a1d3b166
Revises: 66deb4b313d1
Create Date: 2025-04-15 17:06:34.822360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e50a1d3b166'
down_revision: Union[str, None] = '66deb4b313d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'parameters',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('parent_id', sa.Integer, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('min_range', sa.Float, nullable=False),
        sa.Column('max_range', sa.Float, nullable=False),
        sa.Column('protocol', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),

    )


def downgrade() -> None:
    op.drop_table('parameters')
