"""the status column

Revision ID: 5df1a40f7999
Revises: cbc3b2ff1b49
Create Date: 2026-08-17 09:28:32.050105

"""
from typing import Sequence, Union
from sqlalchemy.dialects import postgresql
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5df1a40f7999'
down_revision: Union[str, Sequence[str], None] = 'cbc3b2ff1b49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
            'users',
            sa.Column(
                'status',
                postgresql.ENUM(
                    'active',
                    'inactive',
                    'expired',
                    name='user_status',
                    create_type=False
                ),
                nullable=False
            )
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users','status')
