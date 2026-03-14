import sqlite3
import pandas as pd

# connect to database
conn = sqlite3.connect("database/expenses.db")

# read table
df = pd.read_sql_query("SELECT * FROM expenses", conn)

# export to csv
df.to_csv("data/expenses_live.csv", index=False)

conn.close()

print("Data exported successfully!")