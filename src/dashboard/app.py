import duckdb
import numpy as np
import streamlit as st

#1. Configure the page settings
st.set_page_config(page_title="Inventory Dashboard", layout="wide")
st.title("Live Inventory Control Center")

#2. Build the interactive sidebar
st.sidebar.header("Engine Settings")
safety_buffer = st.sidebar.slider("Safety Stock Buffer", min_value=0, max_value=50, value=10)

#3 Connecet to DuckDB and fetch the latest inventory data
@st.cache_data
def load_data():
    conn = duckdb.connect("data/inventory.db")
    query = """
    SELECT
        p.product_name,
        p.sku,
        i.stock_quantity AS current_stock,
        p.lead_time_days,
        p.wholesale_cost
    FROM products_catalog p
    JOIN inventory_levels i ON p.sku = i.sku
    WHERE i.timestamp =(SELECT MAX(timestamp) FROM inventory_levels)
    """

    return conn.execute(query).df()

df = load_data()

#4. Apply Business Logic using the dynamic slider variable
df['reorder_threshold'] = (df['lead_time_days'] * 5) + safety_buffer
df['action_required'] =np.where(df['current_stock'] <= df['reorder_threshold'], 'REORDER', 'HEALTHY')
df['est_restock_cost'] = np.where(df['action_required'] == 'REORDER', df['wholesale_cost'] *50,0)

#5. Build the Visuals
total_reorders = len(df[df['action_required'] == 'REORDER'])
total_cost = df['est_restock_cost'].sum()

col1, col2 = st.columns(2)
col1.metric("Itmes Requiring Reorder", total_reorders)
col2.metric("Est. Retock Capital", f"${total_cost:.2f}")

st.markdown("---")

st.subheader("Action Required")
action_df = df[df['action_required'] == 'REORDER']
if action_df.empty:
    st.success("All stock levels are healthy! No reorders needed.")
else: 
    st.dataframe(action_df[['product_name', 'current_stock', 'reorder_threshold']], use_container_width=True)


st.subheader("Healthy Stock")
st.dataframe(df[df['action_required'] == 'HEALTHY'][['product_name', 'current_stock', 'reorder_threshold']], use_container_width=True)

#--- LINE CHART CODE ---

st.markdown("---")
st.subheader("30-Day Trend Analysis")

#1. The UI Dropdown
# We grab the unique product names from the dataframe we already built above
selected_product = st.selectbox("Select an item to view its history:", df['product_name'].unique())

#2 . The Translation
# The database needs the SKU to search, but the user clicked a product name.
# This line finds the matching SKU for the selected product.
selected_sku = df[df['product_name'] == selected_product]['sku'].iloc[0]

#3. The Database Query
@st.cache_data
def load_history(sku):
    conn = duckdb.connect("data/inventory.db")
    # We use an f-string to inject the specific SKU into our SQL query
    query = f"""
        SELECT timestamp, stock_quantity 
        FROM inventory_levels 
        WHERE sku = '{sku}'
        ORDER BY timestamp ASC
    """
    return conn.execute(query).df()

history_df = load_history(selected_sku)

#4. The Chart
# Streamlit's line_chart automatically uses the DataFrame's "index" as the X-axis
# So we set the timestamp to be the index before handing it to Streamlit
history_df = history_df.set_index('timestamp')
st.line_chart(history_df)