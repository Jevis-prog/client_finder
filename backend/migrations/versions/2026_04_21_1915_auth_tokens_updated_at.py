"""auth tokens updated_at

Revision ID: 7c6b5a4d3e2f
Revises: 9f1a2b3c4d5e
Create Date: 2026-04-21 19:15:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7c6b5a4d3e2f'
down_revision: Union[str, Sequence[str], None] = '9f1a2b3c4d5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'auth_tokens',
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_column('auth_tokens', 'updated_at')
