import sqlite3
from django.conf import settings
from typing import Any

db_name: str = 'db.sqlite3'


def create_database() -> str:
    db_path = settings.BASE_DIR / db_name
    conn = sqlite3.connect(db_path)
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
        category_id INTEGER,
        type TEXT NOT NULL,
        price INTEGER DEFAULT 0,
        quantity_available INTEGER DEFAULT 0,
        FOREIGN KEY (category_id) REFERENCES Category(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()
    return db_path


def execute_query(query: str, parameters=None):
    result = None

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("BEGIN TRANSACTION")
    try:
        if parameters:
            cur.execute(query, parameters)
        else:
            cur.execute(query)

        if query.find("SELECT") >= 0:
            result = cur.fetchall()
            if len(result) == 1:
                return result[0]
        cur.execute("COMMIT")
    except Exception as e:
        cur.execute("ROLLBACK")
        raise e

    conn.commit()
    conn.close()

    return result
