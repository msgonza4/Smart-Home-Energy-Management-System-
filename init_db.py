import sqlite3

conn = sqlite3.connect('energy.db')  # Create or connect to the DB
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS energy_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id TEXT NOT NULL,
    energy_consumption REAL NOT NULL
)
''')

conn.commit()
conn.close()
