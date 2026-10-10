import random
from datetime import datetime, timedelta

import duckdb

# Connect to the database
conn = duckdb.connect("data/inventory.db")

# 1. Clear out any old test data to start fresh
conn.execute("DELETE FROM products_catalog")
conn.execute("DELETE FROM inventory_levels")

# 2. Define our mock data for products
# Format: (SKU, Product Name, Wholesale Cost, Lead Time in Days)
catalog = [
    ("SKU-1001", "Red Bull Energy Drink, 12oz", 1.85, 2),
    ("SKU-1002", "Monster Energy Drink, 16oz", 2.49, 3),
    ("SKU-1003", "Rockstar Energy Drink, 16oz", 2.99, 4),
    ("SKU-1004", "Takis Fuego Rolled Tortilla Chips, 9.9 oz", 2.10, 3),
    ("SKU-1005", "Marlboro Red Box", 5.75, 1),
]

# 3. Inject the catalog into the Products table
for item in catalog:
    conn.execute("INSERT INTO products_catalog VALUES (?, ?, ?, ?)", item)

print(f"Injected {len(catalog)} products into the catalog.")

# 4. Generate 30 days of simulated inventory history
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Track the running stock levels for each iteem in the catalog
# We will start with a random initial stock level for each product and then simulate daily changes
current_stock = {
    "SKU-1001": random.randint(40, 60),
    "SKU-1002": random.randint(30, 50),
    "SKU-1003": random.randint(50, 80),
    "SKU-1004": random.randint(20, 40),
    "SKU-1005": random.randint(60, 100),
}

records_created = 0
current_date = start_date

# Loop through each of the 30 days
while current_date <= end_date:
    for sku in current_stock.keys():
                # Step A: Record the stock level for the day
        conn.execute(
            "INSERT INTO inventory_levels VALUES (?, ?, ?)",
            (current_date, sku, current_stock[sku]),
        )

        # Step B: SImulate random daily sales (reduce the stock)
        daily_sales = random.randint(1, 12)
        current_stock[sku] -= daily_sales

        # Step C: Prevent negative stock
        if current_stock[sku] <= 5:
            current_stock[sku] += random.randint(30, 50)  # Restock if stock is low

    # Move forward to the next day
    current_date += timedelta(days=1)

print(f"Generated {records_created} daily inventory tracking records.")
print("Mock data generation complete!")
