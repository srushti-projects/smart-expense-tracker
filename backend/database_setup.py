import sqlite3
import os

def init_db():
    db_path = '../database/expenses.db'
    
    # Ensure database directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        profile_pic TEXT DEFAULT 'default.png'
    )
    ''')
    
    # Check if profile_pic column already exists in users table (for existing DBs)
    cursor.execute("PRAGMA table_info(users)")
    user_columns = [col[1] for col in cursor.fetchall()]
    
    if "profile_pic" not in user_columns:
        print("Adding profile_pic column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN profile_pic TEXT DEFAULT 'default.png'")
    
    # Check if user_id column already exists
    cursor.execute("PRAGMA table_info(expenses)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "user_id" not in columns:
        print("Adding user_id column to expenses table...")
        cursor.execute("ALTER TABLE expenses ADD COLUMN user_id INTEGER DEFAULT 1 REFERENCES users(id)")
    else:
        print("user_id column already exists.")
        
    conn.commit()
    conn.close()
    print("Database updated successfully!")

if __name__ == '__main__':
    init_db()
