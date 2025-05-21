"""estado_inicial

Revision ID: 12aa01641568
Revises: 69fba27b376e
Create Date: 2025-05-20 17:42:12.996215

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12aa01641568'
down_revision: Union[str, None] = '69fba27b376e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
