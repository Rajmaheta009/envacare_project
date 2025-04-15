"""test

Revision ID: 7a5706e7a57a
Revises: 5504973554f5
Create Date: 2025-04-15 17:11:15.635235


'5504973554f5'
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a5706e7a57a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('city',sa.String))

def downgrade() -> None:
    """Downgrade schema."""
    pass
