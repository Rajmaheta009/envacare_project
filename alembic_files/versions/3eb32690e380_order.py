"""order

Revision ID: 3eb32690e380
Revises: e94a6cf82b8d
Create Date: 2025-04-15 17:04:51.632239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3eb32690e380'
down_revision: Union[str, None] = 'e94a6cf82b8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'order',
        sa.Column('id',sa.Integer,autoincrement=True,primary_key=True),
        sa.Column('customer_id',sa.Integer,sa.ForeignKey('customer.id'),nullable=False),
        sa.Column('comment', sa.Text, nullable=True),
        sa.Column('doc', sa.String, nullable=True),
        sa.Column('status',sa.Boolean,default="Quotation Check"),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('is_delete',sa.Boolean,default=False),
        sa.CheckConstraint(
            'comment IS NOT NULL OR doc IS NOT NULL',
            name='check_comment_or_doc_not_null'),

    )


def downgrade() -> None:
    op.drop_table('order')
