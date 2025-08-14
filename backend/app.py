from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import random

app = Flask(__name__)
CORS(app)

DATABASE = 'quotes.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/quote")
def get_quote():
    conn = get_db_connection()
    quote_row = conn.execute('SELECT text FROM quotes ORDER BY RANDOM() LIMIT 1').fetchone()
    conn.close()
    if quote_row:
        return jsonify({"quote": quote_row['text']})
    else:
        return jsonify({"quote": "No quotes available."})
    
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

@app.route("/quotes")
def get_all_quotes():
    conn = get_db_connection()
    quotes = conn.execute('SELECT id, text FROM quotes').fetchall()
    conn.close()
    return jsonify([{"id": q["id"], "text": q["text"]} for q in quotes])

@app.route("/quote/<int:quote_id>", methods=['PUT'])
def update_quote(quote_id):
    data = request.get_json()
    new_text = data.get('text')
    if not new_text:
        return jsonify({"error": "No quote provided"}), 400

    conn = get_db_connection()
    conn.execute('UPDATE quotes SET text = ? WHERE id = ?', (new_text, quote_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Quote updated!"})

@app.route("/quote/<int:quote_id>", methods=['DELETE', 'OPTIONS'])
def delete_quote(quote_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM quotes WHERE id = ?', (quote_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Quote deleted!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

