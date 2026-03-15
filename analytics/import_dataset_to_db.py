import pandas as pd
import sqlite3

# load kaggle dataset
df = pd.read_csv("data/expenses.csv")

# rename columns to match database
df.columns = ["date","category","amount","payment_mode","month"]

# connect database
conn = sqlite3.connect("database/expenses.db")

# insert data
df.to_sql("expenses", conn, if_exists="append", index=False)

conn.close()

print("Dataset imported successfully!")