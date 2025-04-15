"""order_perameter

Revision ID: 389b60d3f9d0
Revises: 2e50a1d3b166
Create Date: 2025-04-15 17:07:04.665556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '389b60d3f9d0'
down_revision: Union[str, None] = '2e50a1d3b166'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.create_table(
        'order_parameters',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('quotation_id', sa.Integer, nullable=False),
        sa.Column('parameter_id', sa.Integer, nullable=False),
        sa.Column('cost', sa.Float, nullable=True),
        sa.Column('result', sa.String(255), nullable=True),
        sa.Column('is_delete', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default=sa.text('true')),
    )


def downgrade() -> None:
    op.drop_table('order_parameters')
