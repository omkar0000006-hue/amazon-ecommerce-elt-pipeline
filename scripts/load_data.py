import pandas as pd
import duckdb
import os

os.makedirs("output", exist_ok=True)

customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders.csv")

conn = duckdb.connect("output/ecommerce.db")

conn.register("customers_df", customers)
conn.register("products_df", products)
conn.register("orders_df", orders)

conn.execute("""
CREATE OR REPLACE TABLE raw_customers AS
SELECT * FROM customers_df
""")

conn.execute("""
CREATE OR REPLACE TABLE raw_products AS
SELECT * FROM products_df
""")

conn.execute("""
CREATE OR REPLACE TABLE raw_orders AS
SELECT * FROM orders_df
""")

print("Raw Data Loaded Successfully")

conn.close()