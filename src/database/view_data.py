import duckdb

#1. Connect to the warehouse
conn = duckdb.connect("data/inventory.db")

#2 Query the Products Catalog and convert it to a pandas dataframe for clean printing
print("===Products Catalog ===")
products = conn.execute("SELECT * FROM products_catalog").df()
print(products)

print("\n=== LIVE INVENTORY (First 10 Records) ===")

#3. Query the Inventory Levelas (just the first 10 rows so we dont flood the console)
inventory = conn.execute ("SELECT * FROM inventory_levels LIMIT 10").df()
print(inventory)

#4. Prove the total record count
total_records = conn.execute("SELECT COUNT(*) FROM inventory_levels").fetchone()[0]
print(f"\nTotal inventory records safely stored in DuckDB: {total_records}")