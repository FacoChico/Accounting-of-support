import sqlite3

from ..models import Category


class CategoryRepository:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def add(self, name: str) -> Category:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Category (name) VALUES (?)', (name,))
        category_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self.get_by_id(category_id)

    def get_all(self) -> list[Category]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Category')
        categories = cursor.fetchall()
        conn.close()
        return [Category(id=row[0], name=row[1]) for row in categories]

    def get_by_id(self, category_id: int) -> Category | None:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Category WHERE id=?', (category_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Category(id=row[0], name=row[1])
        return None

    def get_by_name(self, name: str) -> Category | None:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Category WHERE name=? LIMIT 1', (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Category(id=row[0], name=row[1])
        return None

    def update(self, category_id: int, name: str) -> Category | None:
        category = self.get_by_id(category_id)
        if category is None:
            return None

        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('UPDATE Category SET name=? WHERE id=?', (name, category_id))
        conn.commit()
        conn.close()

        category.name = name
        return category

    def delete(self, category_id: int) -> Category | None:
        category = self.get_by_id(category_id)
        if not category:
            return None
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Category WHERE id=?', (category_id,))
        conn.commit()
        conn.close()
        return category
