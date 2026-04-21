"""broken_messages

Revision ID: 50cda3a3f1c3
Revises: 174ec6408757
Create Date: 2025-08-22 10:11:48.407294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50cda3a3f1c3'
down_revision: Union[str, Sequence[str], None] = '174ec6408757'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema: добавляем статус BROKEN безопасным способом."""
    op.execute(
        "CREATE TYPE processingstatus_new AS ENUM ('PENDING', 'ANALYZED', 'FAILED', 'BROKEN');"
    )
    op.execute(
        """
        ALTER TABLE messages
        ALTER COLUMN processing_status
        TYPE processingstatus_new
        USING CASE
            WHEN processing_status = 'PENDING' THEN 'PENDING'::processingstatus_new
            WHEN processing_status = 'ANALYZED' THEN 'ANALYZED'::processingstatus_new
            WHEN processing_status = 'FAILED' THEN 'FAILED'::processingstatus_new
            ELSE 'PENDING'::processingstatus_new
        END;
        """
    )
    op.execute("DROP TYPE processingstatus;")
    op.execute("ALTER TYPE processingstatus_new RENAME TO processingstatus;")


def downgrade() -> None:
    """Downgrade schema: убираем статус BROKEN."""
    op.execute("CREATE TYPE processingstatus_old AS ENUM ('PENDING', 'ANALYZED', 'FAILED');")
    op.execute(
        """
        ALTER TABLE messages
        ALTER COLUMN processing_status
        TYPE processingstatus_old
        USING CASE
            WHEN processing_status = 'BROKEN' THEN 'PENDING'::processingstatus_old
            WHEN processing_status = 'PENDING' THEN 'PENDING'::processingstatus_old
            WHEN processing_status = 'ANALYZED' THEN 'ANALYZED'::processingstatus_old
            WHEN processing_status = 'FAILED' THEN 'FAILED'::processingstatus_old
            ELSE 'PENDING'::processingstatus_old
        END;
        """
    )
    op.execute("DROP TYPE processingstatus;")
    op.execute("ALTER TYPE processingstatus_old RENAME TO processingstatus;")