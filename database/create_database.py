import sqlite3

with sqlite3.connect("db.sqlite3") as conn:
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS parser_data (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        xpath TEXT NOT NULL);"""
    )
    conn.commit()
