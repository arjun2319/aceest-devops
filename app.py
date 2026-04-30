from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
import os

def get_db_path():
    return os.environ.get("DB_PATH", "aceest.db")

PROGRAMS = {
    "Fat Loss": {"calorie_factor": 22},
    "Muscle Gain": {"calorie_factor": 35},
    "Beginner": {"calorie_factor": 26}
}

def init_db():
    conn = sqlite3.connect(get_db_path())
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            age INTEGER,
            weight REAL,
            program TEXT,
            calories INTEGER
        )
    """)
    conn.commit()
    conn.close()

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "version": "1.0"})

@app.route("/programs")
def programs():
    return jsonify(list(PROGRAMS.keys()))

@app.route("/clients", methods=["GET"])
def get_clients():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM clients").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/clients", methods=["POST"])
def add_client():
    data = request.get_json()
    name = data.get("name", "").strip()
    program = data.get("program", "")
    weight = float(data.get("weight", 0))

    if not name:
        return jsonify({"error": "name required"}), 400
    if program not in PROGRAMS:
        return jsonify({"error": "invalid program"}), 400

    calories = int(weight * PROGRAMS[program]["calorie_factor"])

    conn = sqlite3.connect(get_db_path())
    try:
        conn.execute(
            "INSERT INTO clients (name,age,weight,program,calories) VALUES (?,?,?,?,?)",
            (name, data.get("age", 0), weight, program, calories)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "client already exists"}), 409
    conn.close()
    return jsonify({"message": f"{name} added", "calories": calories}), 201

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)