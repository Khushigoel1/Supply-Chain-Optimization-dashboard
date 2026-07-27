import pandas as pd
import numpy as np
raw_path = "DataCoSupplyChainDataset.csv"
out_csv="supply_chain.csv"
df=pd.read_csv(raw_path,encoding="ISO-8859-1")
print(f"Raw Shape:{df.shape}")
drop_col=["Customer Email","Customer Password","CustomerFname","Customer Lname","Customer Street","Product Description","Product Image","Order Zipcode"]
df=df.drop(columns=[c for c in drop_col if c in df.columns])
#parse data
df["order date (DateOrders)"]=pd.to_datetime(df["order date (DateOrders)"], errors="coerce")
df["shipping date (DateOrders)"]=pd.to_datetime(df["shipping date (DateOrders)"],errors="coerce")

#missing values
num_cols=df.select_dtypes(include=[np.number]).columns.tolist()
for col in num_cols:
    if df[col].isnull().sum()>0:
        df[col]=df[col].fillna(df[col].median())

cat_cols=df.select_dtypes(include=["object"]).columns.tolist()
for col in cat_cols:
    if df[col].isnull().sum()>0:
        df[col]=df[col].fillna("unknown")
df = df.dropna(subset=["order date (DateOrders)"])

#outlier handling
def cap_outliers_iqr(series, k=1.5):
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - k * iqr, q3 + k * iqr
    return series.clip(lower=lower, upper=upper)

def cap_outliers_percentile(series, lower_pct=0.01, upper_pct=0.99):
    lower, upper = series.quantile(lower_pct), series.quantile(upper_pct)
    return series.clip(lower=lower, upper=upper)

# Volume/price fields -> IQR capping
for col in ["Sales", "Order Item Total", "Order Item Quantity", "Product Price"]:
    df[col] = cap_outliers_iqr(df[col])
# Profit/discount fields -> wider percentile capping
# (negative profit is a real business signal, not necessarily an error,
#  so IQR is too aggressive here — percentile cap only trims extremes)
for col in ["Order Profit Per Order", "Order Item Profit Ratio", "Benefit per order", "Order Item Discount"]:
    df[col] = cap_outliers_percentile(df[col])

for col in ["Order Item Quantity", "Product Price", "Sales", "Order Item Total"]:
    df[col] = df[col].clip(lower=0)

#feature engineering
df["order_year"] = df["order date (DateOrders)"].dt.year
df["order_month"] = df["order date (DateOrders)"].dt.month
df["order_week"] = df["order date (DateOrders)"].dt.isocalendar().week.astype(int)
df["order_yearmonth"] = df["order date (DateOrders)"].dt.to_period("M").astype(str)
df["order_dayofweek"] = df["order date (DateOrders)"].dt.day_name()
df["lead_time_days"] = (df["shipping date (DateOrders)"] - df["order date (DateOrders)"]).dt.days.clip(lower=0)

# SAVE
df.to_csv(out_csv, index=False)
print(f"Final clean shape: {df.shape}")
print(f"Saved to {out_csv}")

print(df.columns)