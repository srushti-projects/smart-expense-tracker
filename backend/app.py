from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/add-expense', methods=['POST'])
def add_expense():

    data = request.json

    conn = sqlite3.connect("database/expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO expenses (date, category, amount, payment_mode)
    VALUES (?, ?, ?, ?)
    """, (
        data["date"],
        data["category"],
        data["amount"],
        data["payment_mode"]
    ))

    conn.commit()

    # export data for dashboard
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    df.to_csv("data/expenses_live.csv", index=False)

    conn.close()

    return jsonify({"message": "Expense added successfully"})


@app.route('/expenses', methods=['GET'])
def get_expenses():

    conn = sqlite3.connect("database/expenses.db")
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()

    return df.to_json(orient="records")


if __name__ == "__main__":
    app.run(debug=True)