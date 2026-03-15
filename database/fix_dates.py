import pandas as pd

df = pd.read_csv("data/expenses_live.csv")

# convert existing dates
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# fill missing dates using month column
df["date"] = df["date"].fillna(
    pd.to_datetime("2024-" + df["month"].astype(str) + "-01", errors="coerce")
)

# final format
df["date"] = df["date"].dt.strftime("%Y-%m-%d")

df.to_csv("data/expenses_live.csv", index=False)

print("Dates fixed successfully")
