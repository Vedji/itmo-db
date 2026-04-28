/* Создание таблицы*/
CREATE TABLE nf2_customers (
    customers_id   SERIAL PRIMARY KEY,
    customer_name  TEXT,
    customer_email TEXT,
    customer_phone TEXT
);
CREATE TABLE nf2_orders (
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
/*Миграция*/
INSERT INTO nf2_customers (customer_name, customer_email, customer_phone)
SELECT DISTINCT ON (customer_phone)
    customer_name,
    customer_email,
    customer_phone
FROM nf1_orders
WHERE customer_phone IS NOT NULL;

INSERT INTO nf2_orders (order_id, customers_id, delivery_address, total_amount, status)
SELECT DISTINCT ON (o.order_id)
    o.order_id,
    c.customers_id,
    o.delivery_address,
    o.total_amount,
    o.status
FROM nf1_orders o
JOIN nf2_customers c ON c.customer_phone = o.customer_phone;

INSERT INTO nf2_products (product_name, product_price)
SELECT DISTINCT ON (product_name)
    product_name,
    product_price
FROM nf1_orders
WHERE product_name IS NOT NULL;

INSERT INTO nf2_order_items (order_id, product_id, product_quantity)
SELECT
    o.order_id,
    p.product_id,
    o.product_quantitie::NUMERIC
FROM nf1_orders o
JOIN nf2_products p ON p.product_name = o.product_name;
