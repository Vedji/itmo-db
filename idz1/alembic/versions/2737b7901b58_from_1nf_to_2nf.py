"""from_1nf_to_2nf

Revision ID: 2737b7901b58
Revises: 24199da702cb
Create Date: 2026-04-28 11:47:46.995941

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pathlib import Path


# revision identifiers, used by Alembic.
revision: str = '2737b7901b58'
down_revision: Union[str, Sequence[str], None] = '24199da702cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    orders_table_sql = Path("./././sql/02_to_2nf.sql").read_text(encoding="utf-8").strip()
    op.execute(orders_table_sql)
    op.drop_table("nf1_orders")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
CREATE TABLE nf1_orders (
    order_id          INTEGER,
    order_date        DATE,
    customer_name     TEXT,
    customer_email    TEXT,
    customer_phone    TEXT,
    delivery_address  TEXT,
    total_amount      NUMERIC,
    status            TEXT,
    product_name      TEXT,
    product_price     NUMERIC,
    product_quantitie TEXT
);
""")
    op.execute("""
INSERT INTO nf1_orders (
    order_id,
    order_date,
    customer_name,
    customer_email,
    customer_phone,
    delivery_address,
    total_amount,
    status,
    product_name,
    product_price,
    product_quantitie
)
SELECT
    o.order_id,
    NULL::DATE          AS order_date,  -- отсутствует в NF2, восстановить невозможно
    c.customer_name,
    c.customer_email,
    c.customer_phone,
    o.delivery_address,
    o.total_amount,
    o.status,
    p.product_name,
    p.product_price,
    oi.product_quantity::TEXT
FROM nf2_orders o
JOIN nf2_customers   c  ON c.customers_id = o.customers_id
JOIN nf2_order_items oi ON oi.order_id    = o.order_id
JOIN nf2_products    p  ON p.product_id   = oi.product_id;
""")
    op.drop_table("nf2_order_items")
    op.drop_table("nf2_orders")
    op.drop_table("nf2_products")
    op.drop_table("nf2_customers")
