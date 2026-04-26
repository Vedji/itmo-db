"""create order_raw table

Revision ID: af22f4fa441c
Revises: 
Create Date: 2026-04-26 15:15:10.072664

"""
from typing import Sequence, Union
from alembic import op
from pathlib import Path


# revision identifiers, used by Alembic.
revision: str = 'af22f4fa441c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    orders_table_sql = Path("./././sql/00_orders_raw.sql").read_text(encoding="utf-8").strip()
    op.execute(orders_table_sql)
    content = Path("./././sql/raw_fake_data.sql").read_text(encoding="utf-8").strip()
    op.execute(content)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('orders_raw')
