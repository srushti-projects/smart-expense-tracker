import sqlite3

# Connect to database (creates file if not exists)
conn = sqlite3.connect("expenses.db")

cursor = conn.cursor()

# Create expenses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    payment_mode TEXT,
    month TEXT
)
""")

print("Database and table created successfully!")

conn.commit()
conn.close()