import duckdb

#1. Create and connect to the database file
conn = duckdb.connect('data/inventory.db')

#2. Build the Products Catalog table
conn.execute("""
Create TABLE IF NOT EXISTS products_catalog (
sku VARCHAR PRIMARY KEY,
product_name VARCHAR,
wholesale_cost DECIMAL,
lead_time_days INTEGER)
""")

#3. Build the Live Inventory Tracking table
conn.execute("""CREATE TABLE IF NOT EXISTS inventory_levels (
timestamp TIMESTAMP,
sku VARCHAR,
stock_quantity INTEGER
)
""")

print("Database and tables initialized successfully!")
