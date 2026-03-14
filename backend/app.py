from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Add expense API
@app.route('/add-expense', methods=['POST'])
def add_expense():

    data = request.json

    conn = sqlite3.connect("database/expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (date, category, amount)
        VALUES (?, ?, ?)
    """, (
        data["date"],
        data["category"],
        data["amount"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added successfully"})


# Get all expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():

    conn = sqlite3.connect("database/expenses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    data = cursor.fetchall()

    conn.close()

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)