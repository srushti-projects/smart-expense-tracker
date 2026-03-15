import sqlite3
import pandas as pd

conn = sqlite3.connect("database/expenses.db")

df = pd.read_sql_query("SELECT * FROM expenses", conn)

print(df.head())
print("\nColumns:", df.columns)

conn.close()