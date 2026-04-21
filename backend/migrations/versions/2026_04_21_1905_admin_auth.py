"""admin auth

Revision ID: 9f1a2b3c4d5e
Revises: 300ca1bd82bd
Create Date: 2026-04-21 19:05:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '9f1a2b3c4d5e'
down_revision: Union[str, Sequence[str], None] = '300ca1bd82bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'admin_users',
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
    )
    op.create_table(
        'auth_tokens',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token'),
        sa.ForeignKeyConstraint(['user_id'], ['admin_users.id']),
    )


def downgrade() -> None:
    op.drop_table('auth_tokens')
    op.drop_table('admin_users')
