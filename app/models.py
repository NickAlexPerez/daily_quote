# app/models.py
from .db import get_db_connection

def get_random_quote():
    conn = get_db_connection()
    row = conn.execute('SELECT text FROM quotes ORDER BY RANDOM() LIMIT 1').fetchone()
    conn.close()
    return row

def insert_quote(text):
    conn = get_db_connection()
    conn.execute('INSERT INTO quotes (text) VALUES (?)', (text,))
    conn.commit()
    conn.close()

def get_all_quotes():
    conn = get_db_connection()
    quotes = conn.execute('SELECT id, text FROM quotes').fetchall()
    conn.close()
    return quotes

def update_quote(quote_id, new_text):
    conn = get_db_connection()
    conn.execute('UPDATE quotes SET text = ? WHERE id = ?', (new_text, quote_id))
    conn.commit()
    conn.close()

def delete_quote(quote_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM quotes WHERE id = ?', (quote_id,))
    conn.commit()
    conn.close()

