import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# connect database
conn = sqlite3.connect("database/expenses.db")

# load data
df = pd.read_sql_query("SELECT * FROM expenses", conn)

conn.close()

# convert date column
df["date"] = pd.to_datetime(df["date"])

# create month column
df["month"] = df["date"].dt.month_name()

# category spending
category_spending = df.groupby("category")["amount"].sum()

plt.figure(figsize=(8,5))
sns.barplot(x=category_spending.index, y=category_spending.values)

plt.title("Spending by Category")
plt.xticks(rotation=45)

plt.savefig("analytics/category_spending.png")

# monthly spending
monthly_spending = df.groupby("month")["amount"].sum()

plt.figure(figsize=(8,5))
sns.barplot(x=monthly_spending.index, y=monthly_spending.values)

plt.title("Monthly Spending")

plt.savefig("analytics/monthly_spending.png")

print("Charts generated successfully!")