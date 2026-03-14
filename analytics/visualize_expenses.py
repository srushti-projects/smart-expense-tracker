import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv("data/expenses_clean.csv")

# Spending by Category
category_spending = df.groupby('Category')['Amount'].sum()

plt.figure(figsize=(8,5))
category_spending.plot(kind='bar')
plt.title("Spending by Category")
plt.xlabel("Category")
plt.ylabel("Amount")
plt.tight_layout()
plt.savefig("analytics/category_spending.png")

# Payment Mode Pie Chart
payment_modes = df['Payment_Mode'].value_counts()

plt.figure(figsize=(6,6))
payment_modes.plot(kind='pie', autopct='%1.1f%%')
plt.title("Payment Mode Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig("analytics/payment_modes.png")

# Monthly Spending Trend
monthly_spending = df.groupby('Month')['Amount'].sum()

plt.figure(figsize=(8,5))
monthly_spending.plot(kind='line', marker='o')
plt.title("Monthly Spending Trend")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.tight_layout()
plt.savefig("analytics/monthly_spending.png")

print("Charts generated successfully!")