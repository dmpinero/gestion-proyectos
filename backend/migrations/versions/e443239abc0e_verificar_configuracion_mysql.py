"""verificar_configuracion_mysql

Revision ID: e443239abc0e
Revises: dc0107a620dd
Create Date: 2025-05-20 18:02:35.427429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e443239abc0e'
down_revision: Union[str, None] = 'dc0107a620dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
