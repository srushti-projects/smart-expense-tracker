import sqlite3

conn = sqlite3.connect("database/expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    payment_mode TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")