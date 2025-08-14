from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DATABASE = 'quotes.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/quote")
def get_quote():
    conn = get_db_connection()
    quotes = conn.execute('SELECT text FROM quotes').fetchall()
    conn.close()
    if not quotes:
        return jsonify({"quote": "No quotes available."})
    random_quote = random.choice(quotes)['text']
    return jsonify({"quote": random_quote})

@app.route("/quote", methods=['POST'])
def add_quote():
    data = request.get_json()
    quote_text = data.get('quote')
    if not quote_text:
        return jsonify({"error": "No quote provided"}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO quotes (text) VALUES (?)', (quote_text,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Quote added!"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
