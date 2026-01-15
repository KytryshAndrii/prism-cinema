from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# --- Database configuration ---
DB_HOST = "utils"
DB_NAME = "funnydb"
DB_USER = "postgres"
DB_PASS = "root"

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# --- Endpoints ---

@app.route("/")
def home():
    return "😎 Welcome to FunnyDB Flask API!"

@app.route("/all")
def get_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM funny_table;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route("/random")
def get_random():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM funny_table ORDER BY RANDOM() LIMIT 1;")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(row)

@app.route("/sum")
def get_sum():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(number_value) FROM funny_table;")
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify({"sum": total})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)