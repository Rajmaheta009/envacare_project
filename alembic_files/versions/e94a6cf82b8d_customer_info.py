"""customer_info

Revision ID: e94a6cf82b8d
Revises: 
Create Date: 2025-04-15 16:58:44.941771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e94a6cf82b8d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'customer',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('address', sa.String, nullable=False),
        sa.Column('phone_number', sa.String, nullable=False),
        sa.Column('whatsapp_number', sa.String, nullable=False),
        sa.Column('is_delete', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('customer_request')