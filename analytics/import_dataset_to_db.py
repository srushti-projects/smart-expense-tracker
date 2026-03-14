import pandas as pd
import sqlite3

# load kaggle dataset
df = pd.read_csv("data/expenses.csv")

# connect to database
conn = sqlite3.connect("database/expenses.db")

# insert data into table
df.to_sql("expenses", conn, if_exists="append", index=False)

conn.close()

print("Dataset imported into database successfully!")