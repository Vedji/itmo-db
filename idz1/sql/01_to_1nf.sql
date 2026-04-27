/* Создание таблицы*/
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
/*Миграция*/

INSERT INTO nf1_orders (
    order_id, order_date, customer_name, customer_email, customer_phone,
    delivery_address, total_amount, status,
    product_name, product_price, product_quantitie
)
SELECT
    o.order_id,
    o.order_date,
    o.customer_name,
    o.customer_email,
    o.customer_phone,
    o.delivery_address,
    o.total_amount,
    o.status,
    TRIM(unnest(string_to_array(o.product_names,      ','))) AS product_name,
    TRIM(unnest(string_to_array(o.product_prices,     ',')))::NUMERIC AS product_price,
    TRIM(unnest(string_to_array(o.product_quantities, ','))) AS product_quantitie
FROM orders_raw o;