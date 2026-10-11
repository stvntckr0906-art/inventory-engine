Inventory Control Engine
[View the Live Dashboard Here](https://your-custom-url.streamlit.app)

A full-stack, data-driven dashboard for tracking warehouse stock levels, visualizing historical trends, and automating reorder alerts.

The Business Problem

Static spreadsheets and manual inventory tracking often lead to costly stockouts or bloated warehouse shelves. Supply chain managers need real-time visibility into their burn rates and a dynamic way to calculate reorder thresholds based on changing supplier lead times.

The Solution

This project is an end-to-end data pipeline and interactive dashboard that solves this by replacing static math with dynamic, adjustable logic. It ingests historical data, calculates required safety buffers on the fly, and clearly separates "Healthy" stock from items requiring immediate capital investment.

Architecture & Tech Stack

This project uses a decoupled data logic and presentation layer, built entirely in Python:

Frontend (UI/UX): Streamlit – Chosen for its rapid prototyping capabilities and Python-native state management, allowing the UI to react instantly to data changes.

Data Processing: Pandas – Handles the vectorized business logic, calculating dynamic reorder thresholds ((lead_time * 5) + safety_buffer).

Storage: DuckDB – A high-performance, in-process analytical SQL engine used to query millions of rows of historical data in milliseconds.

Environment & Tooling: Managed via uv for lightning-fast dependency resolution, with strict PEP 8 compliance enforced by Ruff.

Key Features

Dynamic Capital Forecasting: An interactive "Safety Stock Buffer" slider that instantly recalculates required reorder capital across the entire database.

Automated Triage: Automatically splits inventory into action-oriented data tables (Action Required vs Healthy Stock).

Historical Trend Analysis: A dropdown-driven line chart that securely queries the DuckDB backend to visualize 30 days of historical stock movement for any selected SKU.

 How to Run Locally

1. Clone the repository and navigate to the project folder:

git clone https://github.com/your-username/inventory-engine.git
cd inventory-engine


2. Install dependencies (using uv):

uv add streamlit pandas duckdb numpy


3. Launch the dashboard:

uv run streamlit run src/dashboard/app.py


The dashboard will automatically open in your default web browser at http://localhost:8501.

Designed and engineered by Steven Tucker