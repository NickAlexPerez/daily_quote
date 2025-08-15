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

def get_all_tags():
    conn = get_db_connection()
    tags = conn.execute('SELECT id, name FROM tags').fetchall()
    conn.close()
    return tags

def insert_tag(name):
    conn = get_db_connection()
    conn.execute('INSERT INTO tags (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def update_tag(tag_id, new_name):
    conn = get_db_connection()
    conn.execute('UPDATE tags SET name = ? WHERE id = ?', (new_name, tag_id))
    conn.commit()
    conn.close()

def delete_tag(tag_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tags WHERE id = ?', (tag_id,))
    conn.commit()
    conn.close()

def get_quote_tags(quote_id):
    conn = get_db_connection()
    tags = conn.execute('SELECT t.id, t.name FROM tags t JOIN quote_tags qt ON t.id = qt.tag_id WHERE qt.quote_id = ?', (quote_id,)).fetchall()
    conn.close()
    return tags

def add_tag_to_quote(quote_id, tag_id):
    conn = get_db_connection()
    conn.execute('INSERT INTO quote_tags (quote_id, tag_id) VALUES (?, ?)', (quote_id, tag_id))
    conn.commit()
    conn.close()

def remove_tag_from_quote(quote_id, tag_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM quote_tags WHERE quote_id = ? AND tag_id = ?', (quote_id, tag_id))
    conn.commit()
    conn.close()

def get_available_tags_for_quote(quote_id):
    conn = get_db_connection()
    tags = conn.execute('SELECT t.id, t.name FROM tags t WHERE t.id NOT IN (SELECT tag_id FROM quote_tags WHERE quote_id = ?)', (quote_id,)).fetchall()
    conn.close()
    return tags
