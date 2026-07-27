import pandas as pd
import numpy as np
from scipy.stats import norm
forecast_path="forecast_demand.csv"
clean_path="supply_chain.csv"
out_path="inventory_recommendation.csv"
service_level=0.95
order_cost=50
holding_cost_pct=0.20
forecast_df=pd.read_csv(forecast_path,parse_dates=["week_start"])
clean_df=pd.read_csv(clean_path,parse_dates=["order date (DateOrders)"])
lead_time_stats=(
    clean_df.groupby("Category Name")["lead_time_days"].agg(["mean","std"]).reset_index().rename(columns={"mean":"lead_time_mean","std":"lead_time_std"}))
lead_time_stats["lead_time_std"]=lead_time_stats["lead_time_std"].fillna(0)
price_stats=(
    clean_df.groupby("Category Name")["Product Price"].mean().reset_index().rename(columns={"Product Price":"avg_unit_price"})
)
future_demand=forecast_df[forecast_df["is_forecast"]].copy()
demand_stats=(
    future_demand.groupby("Category Name")["forecast_demand"]
    .agg(["mean","std"])
    .reset_index() 
    .rename(columns={"mean":"avg_weekly_demand","std":"demand_std"})
)
demand_stats["demand_std"]=demand_stats["demand_std"].fillna(0)
inv=demand_stats.merge(lead_time_stats,on="Category Name",how="left")
inv= inv.merge(price_stats,on="Category Name",how="left")
inv["lead_time_weeks"]=inv["lead_time_mean"]/7
inv["lead_time_weeks_std"]=inv["lead_time_std"]/7
Z= norm.ppf(service_level)
inv["safety_stock"]=Z*np.sqrt(
    (inv["lead_time_weeks"]*inv["demand_std"]**2) + (inv["avg_weekly_demand"]**2*inv["lead_time_weeks_std"]**2)
)
inv["recorder_point"]=(inv["avg_weekly_demand"]*inv["lead_time_weeks"])+ inv["safety_stock"]

inv["annual_demand"]=inv["avg_weekly_demand"]*52
inv["holding_cost_per_unit"]=inv["avg_unit_price"]*holding_cost_pct
inv["eoq"]=np.sqrt((2*inv["annual_demand"]*order_cost)/inv["holding_cost_per_unit"].replace(0,np.nan)
)
inv=inv.round(2)
inv.to_csv(out_path,index=False)
print(f"saved inventory recommendations to {out_path}")
print(inv[["Category Name","avg_weekly_demand","safety_stock","recorder_point","eoq"]].head(10))

