import duckdb
import pandas as pd

#1. Connect to our data warehouse
conn = duckdb.connect("data/inventory.db")

#2. The SQL Brain: Join the catalog and the latest inventory together
query = """
    SELECT
        p.product_name,
        p.sku,
        i.stock_quantity AS current_stock,
        p.lead_time_days,
        p.wholesale_cost
    FROM products_catalog p
    JOIN inventory_levels i ON p.sku = i.sku
    WHERE i.timestamp = (SELECT MAX(timestamp) FROM inventory_levels)
    """

#3 . Execute the query and load it directly into a Pandas Dataframe
df = conn.execute(query).df()

#4. The Business Logic: Calculate if we are in the danger zone for reordering
# We want a safety buffer of 10 items, plus enough stock to survive to lead time days
df['reorder_threshold'] = (df['lead_time_days'] * 5) + 10

#5 Make the decision: If current stock is below the threshold, flag it!
import numpy as np
df['action_required'] = np.where(df['current_stock'] <=df['reorder_threshold'],'REORDER NOW', 'STOCK HEALTHY')

#6 Calculate potential cost if we by 50 units of the flagged items
df['est_restock_cost'] =np.where(df['action_required'] == 'REORDER NOW', df['wholesale_cost'] * 50, 0)

#7 Print the final intelligence report
print("\n=== AUTOMATED DAILY INVENTORY REPORT ===")
#We will only print the columns the store manager actually cares about
report_columns = ['product_name','sku', 'current_stock', 'reorder_threshold', 'action_required', 'est_restock_cost']
print(df[report_columns].to_string(index=False))

total_spend = df['est_restock_cost'].sum()
print(f"\nEstimated Capital Required for Restock: ${total_spend:.2f}\n")

import os
from datetime import datetime

#8. Automated File Export
#Ensure a 'reports' folder exists in our project directory
os.makedirs("reports", exist_ok=True)

#Generate a filename with today's date so we don't overwrite old reports
today_str = datetime.now().strftime("%Y-%m-%d")
export_filepath = f"reports/inventory_action_report_{today_str}.csv"

#Save the DataFrame to a CSV file(dropping the indx numbers for a cleaner report)
df[report_columns].to_csv(export_filepath, index=False)

print(f"Report exported successfully to: {export_filepath}\n")