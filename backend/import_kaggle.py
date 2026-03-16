import sqlite3
import pandas as pd
from werkzeug.security import generate_password_hash
import os

DB_PATH = "../database/expenses.db"
from datetime import datetime
import pandas as pd

def import_kaggle_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create a demo user for the Kaggle data
    demo_username = "demo"
    demo_password = generate_password_hash("demo123")
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (demo_username, demo_password))
        user_id = cursor.lastrowid
        print(f"Created demo user with ID: {user_id}")
    except sqlite3.IntegrityError:
        cursor.execute("SELECT id FROM users WHERE username = ?", (demo_username,))
        user_id = cursor.fetchone()[0]
        print(f"Demo user already exists with ID: {user_id}")
        
        # Clear existing expenses for the demo user to avoid duplicates if run multiple times
        cursor.execute("DELETE FROM expenses WHERE user_id = ?", (user_id,))
        print("Cleared existing expenses for demo user.")

    # Load Kaggle data
    csv_path = "../data/expenses_clean.csv"
    if not os.path.exists(csv_path):
        print(f"Could not find CSV at {csv_path}")
        return

    df = pd.read_csv(csv_path)
    
    # Calculate date shift so the latest expense is exactly "today"
    df['Date'] = pd.to_datetime(df['Date'])
    max_date = df['Date'].max()
    today = datetime.now()
    delta = today - max_date
    df['shifted_date'] = df['Date'] + delta
    
    inserted_count = 0
    for _, row in df.iterrows():
        try:
            cursor.execute("""
            INSERT INTO expenses (date, category, amount, payment_mode, user_id)
            VALUES (?, ?, ?, ?, ?)
            """, (
                row["shifted_date"].strftime('%Y-%m-%d'),
                row["Category"],
                float(row["Amount"]),
                row["Payment_Mode"],
                user_id
            ))
            inserted_count += 1
        except Exception as e:
            print(f"Error inserting row: {e}")
            
    conn.commit()
    conn.close()
    
    print(f"Successfully imported {inserted_count} expense records for demo user '{demo_username}'.")

if __name__ == "__main__":
    import_kaggle_data()
