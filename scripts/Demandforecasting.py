import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from prophet import Prophet
in_path="supply_chain.csv"
out_path="forecast_demand.csv"
forecast_horizon_weeks=12
min_weeks_for_prophet=20
df=pd.read_csv(in_path,parse_dates=["order date (DateOrders)"])
df["week_start"]=df["order date (DateOrders)"].dt.to_period("W").dt.start_time
weekly=(
df.groupby(["Category Name","week_start"])["Order Item Quantity"]
.sum()
.reset_index()
.rename(columns={"Order Item Quantity":"units_demand"})
)
all_forecasts=[]
for category,grp in weekly.groupby("Category Name"):
    grp=grp.sort_values("week_start").reset_index(drop=True)
    n_weeks=len(grp)
    if n_weeks>= min_weeks_for_prophet:
        prophet_df = grp.rename(columns={"week_start": "ds", "units_demand" :"y"})
        model=Prophet(weekly_seasonality=False,yearly_seasonality=True,seasonality_mode="additive",interval_width=0.8)
        model.fit(prophet_df)
        future=model.make_future_dataframe(periods=forecast_horizon_weeks,freq="W")
        fcst=model.predict(future)
        result=fcst[["ds","yhat","yhat_lower"]].rename(columns={"ds":"week_start","yhat":"forecast_demand","yhat_lower":"forecast_lower","yhat_upper":"forecast_upper"})
        result["Category Name"]=category
        result["model_used"]="Prophet"
        result=result.merge(grp,on="week_start",how="left")
    else:
        avg_demand=grp["units_demand"].mean() if n_weeks>0 else 0
        last_week=grp["week_start"].max() if n_weeks>0 else weekly["week_start"].max()
        future_weeks=pd.date_range(start=last_week + pd.Timedelta(weeks=1),periods=forecast_horizon_weeks,freq="W")
        hist_part=grp.copy()
        hist_part["forecast_demand"]=hist_part["units_demand"]
        hist_part["forecast_lower"]=hist_part["units_demand"]
        hist_part["forecast_upper"]=hist_part["units_demand"]
        future_part=pd.DataFrame({"week_start":future_weeks,"units_demand":np.nan, 
                                 "forecast_demand":avg_demand,"forcast_lower":avg_demand*0.7,"forecast_demand":avg_demand*1.3})
        result=pd.concat([hist_part,future_part],ignore_index=True)
        result["Category Name"]=category
        result["model_used"]="MovingAverage"
    all_forecasts.append(result)
forecast_df=pd.concat(all_forecasts,ignore_index=True)
forecast_df["forecast_demand"]=forecast_df["forecast_demand"].clip(lower=0)
forecast_df["forecast_lower"]=forecast_df["forecast_lower"].clip(lower=0)
forecast_df["is_forecast"]=forecast_df["units_demand"].isna()
forecast_df=forecast_df.sort_values(["Category Name","week_start"])
forecast_df.to_csv(out_path, index=False) 
print(f"saved forecast to {out_path}")
                                   
