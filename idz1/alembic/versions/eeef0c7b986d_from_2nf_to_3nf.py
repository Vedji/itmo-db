"""from_2nf_to_3nf

Revision ID: eeef0c7b986d
Revises: 2737b7901b58
Create Date: 2026-04-28 12:40:16.941707

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from pathlib import Path


# revision identifiers, used by Alembic.
revision: str = 'eeef0c7b986d'
down_revision: Union[str, Sequence[str], None] = '2737b7901b58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    orders_table_sql = Path("./././sql/03_to_3nf.sql").read_text(encoding="utf-8").strip()
    op.execute(orders_table_sql)
    op.drop_table("nf2_order_items")
    op.drop_table("nf2_orders")
    op.drop_table("nf2_products")
    op.drop_table("nf2_customers")



def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
CREATE TABLE nf2_customers (  -- +
    customers_id   SERIAL PRIMARY KEY,
    customer_name  TEXT,
    customer_email TEXT,
    customer_phone TEXT
);
CREATE TABLE nf2_orders (  -- +
    order_id         INTEGER PRIMARY KEY NOT NULL,
    customers_id     INTEGER REFERENCES nf2_customers(customers_id) NOT NULL,
    delivery_address TEXT,
    total_amount     NUMERIC,
    status           TEXT
);
CREATE TABLE nf2_products (
    product_id    SERIAL PRIMARY KEY,
    product_name  TEXT,
    product_price NUMERIC
);
CREATE TABLE nf2_order_items (
    order_id         INTEGER NOT NULL REFERENCES nf2_orders(order_id),
    product_id       INTEGER NOT NULL REFERENCES nf2_products(product_id),
    product_quantity NUMERIC,
    CONSTRAINT pk_order_items PRIMARY KEY (order_id, product_id)
);
INSERT INTO nf2_customers (customers_id, customer_name, customer_email, customer_phone)
SELECT customers_id, customer_name, customer_email, customer_phone FROM nf3_customers;
INSERT INTO nf2_orders (order_id, customers_id, total_amount, status, delivery_address)
SELECT order_id, a.customers_id, total_amount, status, delivery_address 
FROM nf3_orders a RIGHT JOIN nf3_addresses b ON a.addresses_id = b.addresses_id;
INSERT INTO nf2_products (product_id, product_name, product_price)
SELECT product_id, category_name, product_price
FROM nf3_products a RIGHT JOIN categories b ON a.category_id = b.category_id;
INSERT INTO nf2_order_items (order_id, product_id, product_quantity)
SELECT order_id, product_id, product_quantity 
FROM nf3_order_items;
""")
    op.drop_table("nf3_order_items")
    op.drop_table("nf3_products")
    op.drop_table("categories")
    op.drop_table("nf3_orders")
    op.drop_table("nf3_addresses")
    op.drop_table("nf3_customers")
