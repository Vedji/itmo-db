/* Создание таблицы*/
CREATE TABLE nf3_customers (
    customers_id   SERIAL PRIMARY KEY,
    customer_name  TEXT,
    customer_email TEXT,
    customer_phone TEXT
);
CREATE TABLE nf3_addresses (
    addresses_id     SERIAL PRIMARY KEY,
    customers_id     INTEGER NOT NULL REFERENCES nf3_customers(customers_id),
    delivery_address TEXT
);
CREATE TABLE nf3_orders (
    order_id     INTEGER PRIMARY KEY NOT NULL,
    customers_id INTEGER NOT NULL REFERENCES nf3_customers(customers_id),
    addresses_id INTEGER NOT NULL REFERENCES nf3_addresses(addresses_id),
    total_amount NUMERIC,
    status       TEXT
);
CREATE TABLE categories (
    category_id   SERIAL PRIMARY KEY,
    category_name TEXT
);
CREATE TABLE nf3_products (
    product_id    SERIAL PRIMARY KEY,
    category_id   INTEGER REFERENCES categories(category_id),  -- nullable
    product_price NUMERIC
);
CREATE TABLE nf3_order_items (
    order_id         INTEGER NOT NULL REFERENCES nf3_orders(order_id),
    product_id       INTEGER NOT NULL REFERENCES nf3_products(product_id),
    product_quantity NUMERIC,
    CONSTRAINT pk_nf3_order_items PRIMARY KEY (order_id, product_id)
);
/*Миграция*/
INSERT INTO nf3_customers (customers_id, customer_name, customer_email, customer_phone)
SELECT customers_id, customer_name, customer_email, customer_phone
FROM nf2_customers;
INSERT INTO nf3_addresses (customers_id, delivery_address)
SELECT DISTINCT o.customers_id, o.delivery_address
FROM nf2_orders o
WHERE o.delivery_address IS NOT NULL;
INSERT INTO nf3_orders (order_id, customers_id, addresses_id, total_amount, status)
SELECT
    o.order_id,
    o.customers_id,
    a.addresses_id,
    o.total_amount,
    o.status
FROM nf2_orders o
JOIN nf3_addresses a
    ON a.customers_id     = o.customers_id
    AND a.delivery_address = o.delivery_address;
INSERT INTO categories (category_name)
SELECT DISTINCT product_name
FROM nf2_products
WHERE product_name IS NOT NULL;
INSERT INTO nf3_products (product_id, category_id, product_price)
SELECT
    p.product_id,
    c.category_id,
    p.product_price
FROM nf2_products p
LEFT JOIN categories c ON c.category_name = p.product_name;
INSERT INTO nf3_order_items (order_id, product_id, product_quantity)
SELECT order_id, product_id, product_quantity
FROM nf2_order_items;
/*Сброс секвенсов*/
SELECT setval('nf3_customers_customers_id_seq', (SELECT MAX(customers_id) FROM nf3_customers));
SELECT setval('nf3_addresses_addresses_id_seq', (SELECT MAX(addresses_id) FROM nf3_addresses));
SELECT setval('nf3_products_product_id_seq',    (SELECT MAX(product_id)   FROM nf3_products));
SELECT setval('categories_category_id_seq',     (SELECT MAX(category_id)  FROM categories));
