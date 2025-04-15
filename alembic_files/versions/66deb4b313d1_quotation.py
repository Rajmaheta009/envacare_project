"""quotation

Revision ID: 66deb4b313d1
Revises: 3eb32690e380
Create Date: 2025-04-15 17:06:07.521142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66deb4b313d1'
down_revision: Union[str, None] = '3eb32690e380'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'quotations',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('order_id', sa.Integer, nullable=False),
        sa.Column('pdf_url', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),

    )


def downgrade() -> None:
    op.drop_table('quotations')
