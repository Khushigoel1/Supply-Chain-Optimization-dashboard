import numpy as np
import pandas as pd
clean_data_path="supply_chain.csv"
out_path="bottleneck_analysis.csv"
df=pd.read_csv(clean_data_path,parse_dates=["order date (DateOrders)"])
bottlenecks=(df.groupby(["Shipping Mode","Order Region"])
     .agg(total_orders=("Order Id","count"),
       late_orders=("Late_delivery_risk","sum"),
       avg_lead_time=("lead_time_days","mean"),
       avg_profit=("Order Profit Per Order","mean"),)
    .reset_index()
)
bottlenecks["late_rate_pct"]=(bottlenecks["late_orders"]/bottlenecks["total_orders"]*100).round(2)
bottlenecks["avg_lead_time"]=bottlenecks["avg_lead_time"].round(2)
bottlenecks["avg_profit"]=bottlenecks["avg_profit"].round(2)
late_threshold=bottlenecks["late_rate_pct"].median()
profit_threshold=bottlenecks["avg_profit"].median()
bottlenecks["is_bottleneck"]=((bottlenecks["late_rate_pct"]>late_threshold) & (bottlenecks["avg_profit"]<profit_threshold))
bottlenecks=bottlenecks.sort_values("late_rate_pct",ascending=False)
bottlenecks.to_csv(out_path,index=False)
print(f"saved bottleneck analysis to{out_path}")
print(bottlenecks.head(10))