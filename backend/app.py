from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "database" / "expenses.db"

print(f"Using database at: {DB_PATH}")

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Username already exists"}), 409
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        return jsonify({
            "message": "Login successful",
            "user_id": user['id'],
            "username": user['username'],
            "profile_pic": user['profile_pic'] if 'profile_pic' in user.keys() else 'default.png'
        }), 200
    
    return jsonify({"message": "Invalid username or password"}), 401

@app.route('/upload-profile-pic', methods=['POST'])
def upload_profile_pic():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    user_id = request.form.get('user_id')
    if not user_id:
         return jsonify({"message": "No user ID"}), 400
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
        
    uploads_dir = BASE_DIR.parent / "frontend" / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"user_{user_id}_{file.filename}"
    file_path = uploads_dir / filename
    file.save(str(file_path))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET profile_pic = ? WHERE id = ?", (filename, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Profile picture updated", "profile_pic": filename})


@app.route('/add-expense', methods=['POST'])
def add_expense():
    data = request.json
    user_id = data.get("user_id", 1) # Default to 1 if not provided for backward compat

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO expenses (date, category, amount, payment_mode, user_id)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data["date"],
        data["category"],
        data["amount"],
        data["payment_mode"],
        user_id
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added successfully"})


@app.route('/expenses', methods=['GET'])
def get_expenses():
    user_id = request.args.get('user_id', 1)
    
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM expenses WHERE user_id = ?", conn, params=(user_id,))
    conn.close()

    return df.to_json(orient="records")

@app.route('/dashboard-data', methods=['GET'])
def get_dashboard_data():
    user_id = request.args.get('user_id', 1)
    month_filter = request.args.get('month') # Expecting YYYY-MM
    
    conn = get_db_connection()
    if month_filter:
        # Filter by specific month
        query = """
        SELECT * FROM expenses 
        WHERE user_id = ? AND strftime('%Y-%m', date) = ?
        """
        df = pd.read_sql_query(query, conn, params=(user_id, month_filter))
    else:
        # Default: Last 30 days
        query = """
        SELECT * FROM expenses 
        WHERE user_id = ? AND date >= date('now', '-30 days')
        """
        df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    
    if df.empty:
        return jsonify({
            "category_data": {"labels": [], "values": []},
            "monthly_data": {"labels": [], "values": []},
            "total_expenses": 0
        })
        
    # Aggregate by Category
    category_agg = df.groupby('category')['amount'].sum().reset_index()
    category_labels = category_agg['category'].tolist()
    category_values = category_agg['amount'].tolist()
    
    # Aggregate by Date (Day-by-Day for the last 30 days instead of Month)
    # The user asked for exactly a 1-month trajectory, so daily tracking over 30 days is best
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.strftime('%Y-%m-%d')
    daily_agg = df.groupby('day')['amount'].sum().reset_index().sort_values('day')
    daily_labels = daily_agg['day'].tolist()
    daily_values = daily_agg['amount'].tolist()
    
    total_expenses = float(df['amount'].sum())
    
    return jsonify({
         "category_data": {"labels": category_labels, "values": category_values},
         "monthly_data": {"labels": daily_labels, "values": daily_values},
         "total_expenses": total_expenses
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)