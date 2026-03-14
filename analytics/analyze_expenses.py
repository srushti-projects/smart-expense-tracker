import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/expenses_clean.csv")

print("\nTotal Transactions:", len(df))

# Total spending
total_spending = df['Amount'].sum()
print("\nTotal Spending:", total_spending)

# Average transaction
avg_spending = df['Amount'].mean()
print("\nAverage Transaction:", round(avg_spending,2))

# Top spending category
top_category = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
print("\nSpending by Category:\n")
print(top_category)

# Payment mode distribution
payment_modes = df['Payment_Mode'].value_counts()
print("\nPayment Mode Usage:\n")
print(payment_modes)

# Monthly spending
monthly_spending = df.groupby('Month')['Amount'].sum()
print("\nMonthly Spending:\n")
print(monthly_spending)