CREATE OR REPLACE TABLE dim_customers AS
SELECT
customer_id,
customer_name,
city
FROM raw_customers;

CREATE OR REPLACE TABLE dim_products AS
SELECT
product_id,
product_name,
category,
price
FROM raw_products;

CREATE OR REPLACE TABLE dim_date AS
SELECT DISTINCT
order_date
FROM raw_orders;

CREATE OR REPLACE TABLE fact_sales AS
SELECT
o.order_id,
o.order_date,
o.customer_id,
o.product_id,
o.quantity,
p.price,
(o.quantity * p.price) AS total_amount
FROM raw_orders o
JOIN raw_products p
ON o.product_id = p.product_id;