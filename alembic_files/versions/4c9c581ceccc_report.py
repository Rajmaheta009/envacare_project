"""report

Revision ID: 4c9c581ceccc
Revises: 2d9e9fdefa2b
Create Date: 2025-04-15 17:07:47.817103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c9c581ceccc'
down_revision: Union[str, None] = '2d9e9fdefa2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.create_table(
        'reports',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('order_id', sa.Integer, nullable=False),
        sa.Column('pdf_url', sa.String(500), nullable=False),
        sa.Column('is_delete', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('reports')
