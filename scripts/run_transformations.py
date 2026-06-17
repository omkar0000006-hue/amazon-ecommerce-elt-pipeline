import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import logging
import os



logging.basicConfig(
    filename="etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Pipeline Started")



conn = duckdb.connect(
    "output/ecommerce.db"
)



with open(
    "sql/transformations.sql",
    "r"
) as file:

    sql_script = file.read()

conn.execute(sql_script)

print("Transformations Complete")

logging.info("Transformations Complete")



kpi_report = conn.execute("""
SELECT
COUNT(DISTINCT customer_id) AS total_customers,
COUNT(DISTINCT product_id) AS total_products,
SUM(total_amount) AS total_revenue,
ROUND(AVG(total_amount),2) AS avg_order_value
FROM fact_sales
""").fetchdf()

kpi_report.to_csv(
    "output/kpi_report.csv",
    index=False
)

print("\nKPI Report")
print(kpi_report)



sales_report = conn.execute("""
SELECT
SUM(total_amount) AS total_sales
FROM fact_sales
""").fetchdf()

sales_report.to_csv(
    "output/sales_report.csv",
    index=False
)


top_customers = conn.execute("""
SELECT
c.customer_name,
SUM(f.total_amount) AS total_spent
FROM fact_sales f
JOIN dim_customers c
ON f.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY total_spent DESC
""").fetchdf()

top_customers.to_csv(
    "output/top_customers.csv",
    index=False
)

print("\nTop Customers")
print(top_customers)



customer_rank = conn.execute("""
SELECT
customer_name,
total_spent,
RANK() OVER (
ORDER BY total_spent DESC
) AS customer_rank
FROM (

SELECT
c.customer_name,
SUM(f.total_amount) AS total_spent
FROM fact_sales f
JOIN dim_customers c
ON f.customer_id = c.customer_id
GROUP BY c.customer_name

)
""").fetchdf()

customer_rank.to_csv(
    "output/customer_rank.csv",
    index=False
)



top_products = conn.execute("""
SELECT
p.product_name,
SUM(f.quantity) AS total_quantity
FROM fact_sales f
JOIN dim_products p
ON f.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_quantity DESC
""").fetchdf()

top_products.to_csv(
    "output/top_products.csv",
    index=False
)

print("\nTop Products")
print(top_products)



category_report = conn.execute("""
SELECT
p.category,
SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_products p
ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC
""").fetchdf()

category_report.to_csv(
    "output/revenue_by_category.csv",
    index=False
)



city_report = conn.execute("""
SELECT
c.city,
SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_customers c
ON f.customer_id = c.customer_id
GROUP BY c.city
ORDER BY revenue DESC
""").fetchdf()

city_report.to_csv(
    "output/revenue_by_city.csv",
    index=False
)



daily_sales = conn.execute("""
SELECT
order_date,
SUM(total_amount) AS revenue
FROM fact_sales
GROUP BY order_date
ORDER BY order_date
""").fetchdf()

daily_sales.to_csv(
    "output/daily_sales.csv",
    index=False
)


plt.figure(figsize=(8,5))

plt.bar(
    top_customers["customer_name"],
    top_customers["total_spent"]
)

plt.title("Top Customers")
plt.xlabel("Customer")
plt.ylabel("Amount Spent")

plt.tight_layout()

plt.savefig(
    "output/top_customers.png"
)

plt.close()


plt.figure(figsize=(8,5))

plt.bar(
    top_products["product_name"],
    top_products["total_quantity"]
)

plt.title("Top Products")
plt.xlabel("Product")
plt.ylabel("Quantity Sold")

plt.tight_layout()

plt.savefig(
    "output/top_products.png"
)

plt.close()


plt.figure(figsize=(8,5))

plt.plot(
    daily_sales["order_date"],
    daily_sales["revenue"]
)

plt.title("Daily Revenue Trend")
plt.xlabel("Date")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "output/daily_sales_trend.png"
)

plt.close()

logging.info("Reports Generated")

conn.close()

logging.info("Pipeline Completed")

print("\nReports Generated Successfully")
print("\nPipeline Completed")