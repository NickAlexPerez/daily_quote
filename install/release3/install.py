import sqlite3

conn = sqlite3.connect('quotes.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
''')

c.execute('''
CREATE TABLE IF NOT EXISTS quote_tags (
    quote_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (quote_id, tag_id),
    FOREIGN KEY (quote_id) REFERENCES quotes (id),
    FOREIGN KEY (tag_id) REFERENCES tags (id)
);
''')

conn.commit()
conn.close()

print("Database initialized and seeded.")
