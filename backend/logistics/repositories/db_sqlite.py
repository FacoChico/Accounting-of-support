import sqlite3
from django.conf import settings
from typing import Any

db_name: str = 'db.sqlite3'


def create_database() -> str:
    db_path = settings.BASE_DIR / db_name
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Category (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Logistics (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        price INTEGER DEFAULT 0,
        quantity_available INTEGER DEFAULT 0,
        FOREIGN KEY (category_id) REFERENCES Category(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()
    return db_path
