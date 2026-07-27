<<<<<<< HEAD
📌 Project Overview

This project demonstrates how to build a full-stack supply chain analytics pipeline using the DataCo Smart Supply Chain dataset (180,519 order records). It covers everything from raw data cleaning to an interactive Tableau dashboard that visualizes demand forecasts, inventory risk, delivery bottlenecks, and category profitability.

🎯 Objectives
Clean and preprocess a large, real-world supply chain dataset
Forecast weekly product demand using Facebook Prophet
Optimize inventory levels using Safety Stock, Reorder Point, and EOQ models
Identify supply chain bottlenecks using late delivery and profitability analysis
Build an interactive Tableau dashboard with KPIs, filters, and cross-sheet actions

📊 Dashboard Features

The Tableau dashboard (supply_chain_dashboard.twbx) includes:

📈 KPI Strip (Top)
Total Sales
Total Profit
Average Lead Time
Late Delivery Rate
Total Forecasted Demand (next 12 weeks)
📉 Demand Forecast Line Chart
Historical actual demand vs. Prophet forecast per category
Shaded 80% confidence interval band
Color split: Actual (blue) vs. Forecast (orange)
Filter by Category Name
📦 Inventory Risk Bar Chart
Safety stock per category (bars, colored by EOQ)
Reorder point markers (red dots)
Sorted descending by safety stock
Categories where bar < red dot = stockout risk
🌡 Bottleneck Heatmap
Shipping Mode (rows) × Order Region (columns)
Cell color: red = bottleneck, blue = normal
Tooltip: region, shipping mode, late rate, avg profit, total orders
🌳 Sales by Category Treemap
Block size = total sales volume
Block color = profit margin % (green = profitable, red = loss-making)

📚 Learning Outcomes

Through this project you will learn:

Large-scale data cleaning and outlier handling strategies
Time series forecasting with Facebook Prophet
Statistical inventory optimization (Safety Stock, ROP, EOQ)
Supply chain bottleneck detection using aggregated KPIs
Tableau data modeling (relationships vs joins, multi-source dashboards)
Dashboard design principles (layout, filters, actions, tooltips)

🔮 Future Improvements
Add SKU-level forecasting (currently Category-level)
Implement live TabPy connection for real-time Tableau ↔ Python integration
Schedule pipeline with Apache Airflow for automated daily refresh
Add Customer Lifetime Value (CLV) analysis layer
Build a Streamlit web app as an alternative to Tableau
Extend bottleneck detection with network graph optimization
Add anomaly detection on demand spikes using Isolation Forest
Integrate AI-generated executive summaries via LLM API
=======
# Supply-Chain-Optimization-dashboard
>>>>>>> bf6858cafdba6f502b9dbafb7555b81d233dffa4
