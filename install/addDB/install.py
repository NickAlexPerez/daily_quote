import sqlite3

conn = sqlite3.connect('quotes.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL
)
''')

# Optionally insert some initial quotes
initial_quotes = [
    "The best way to get started is to quit talking and begin doing.",
    "Don’t let yesterday take up too much of today.",
    "It’s not whether you get knocked down, it’s whether you get up.",
    "Success is not in what you have, but who you are."
]

c.executemany('INSERT INTO quotes (text) VALUES (?)',
              [(quote,) for quote in initial_quotes])

conn.commit()
conn.close()

print("Database initialized and seeded.")
