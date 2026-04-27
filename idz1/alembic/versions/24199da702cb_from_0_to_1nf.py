"""from_0_to_1nf

Revision ID: 24199da702cb
Revises: af22f4fa441c
Create Date: 2026-04-26 22:14:21.678399

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pathlib import Path


# revision identifiers, used by Alembic.
revision: str = '24199da702cb'
down_revision: Union[str, Sequence[str], None] = 'af22f4fa441c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    orders_table_sql = Path("./././sql/01_to_1nf.sql").read_text(encoding="utf-8").strip()
    op.execute(orders_table_sql)
    op.drop_table('orders_raw')


def downgrade() -> None:
    """Downgrade schema."""
    orders_table_sql = Path("./././sql/00_orders_raw.sql").read_text(encoding="utf-8").strip()
    op.execute(orders_table_sql)
    op.execute("""
INSERT INTO orders_raw (
    order_id, order_date, customer_name, customer_email, customer_phone,
    delivery_address, total_amount, status,
    product_names, product_prices, product_quantities
)
SELECT
    order_id,
    order_date,
    customer_name,
    customer_email,
    customer_phone,
    delivery_address,
    total_amount,
    status,
    string_agg(product_name,              ', ') AS product_names,
    string_agg(product_price::TEXT,       ', ') AS product_prices,
    string_agg(product_quantitie,         ', ') AS product_quantities
FROM nf1_orders
GROUP BY
    order_id, order_date, customer_name, customer_email, customer_phone,
    delivery_address, total_amount, status;
""")
    op.drop_table('nf1_orders')
