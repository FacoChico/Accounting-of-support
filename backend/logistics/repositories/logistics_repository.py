import sqlite3
from .category_repository import CategoryRepository
from ..models import Logistics


class LogisticsRepository:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.category_repo = CategoryRepository(db_path)

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def add(self, name: str, category_id: int, type: str,
            price: int = 0, quantity_available: int = 0) -> Logistics | None:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO Logistics (name, category_id, type, price, quantity_available)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, category_id, type, price, quantity_available))
        logistics_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self.get_by_id(logistics_id)

    def get_all(self, category_id: int | None = None) -> list[Logistics]:
        conn = self._connect()
        cursor = conn.cursor()
        if category_id is None:
            cursor.execute('SELECT * FROM Logistics')
        else:
            cursor.execute('SELECT * FROM Logistics WHERE category_id = ?', (category_id,))
        logistics = cursor.fetchall()
        conn.close()
        return [
            Logistics(
                id=row[0], name=row[1],
                category=self.get_category(row[2]),
                type=row[3], price=row[4],
                quantity_available=row[5]
            ) for row in logistics
        ]

    def get_by_id(self, logistics_id) -> Logistics | None:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Logistics WHERE id=?', (logistics_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Logistics(
                id=row[0], name=row[1],
                category=self.get_category(row[2]),
                type=row[3], price=row[4],
                quantity_available=row[5]
            )
        return None

    def update(self, logistics_id, name=None, category_id=None,
               type=None, price=None, quantity_available=None) -> Logistics | None:
        logistics = self.get_by_id(logistics_id)
        if not logistics:
            return None
        conn = self._connect()
        cursor = conn.cursor()
        if name:
            cursor.execute('UPDATE Logistics SET name=? WHERE id=?', (name, logistics_id))
        if category_id:
            cursor.execute('UPDATE Logistics SET category_id=? WHERE id=?', (category_id, logistics_id))
        if type:
            cursor.execute('UPDATE Logistics SET type=? WHERE id=?', (type, logistics_id))
        if price is not None:
            cursor.execute('UPDATE Logistics SET price=? WHERE id=?', (price, logistics_id))
        if quantity_available is not None:
            cursor.execute('UPDATE Logistics SET quantity_available=? WHERE id=?', (quantity_available, logistics_id))
        conn.commit()
        conn.close()
        return self.get_by_id(logistics_id)

    def delete(self, logistics_id) -> Logistics | None:
        logistics = self.get_by_id(logistics_id)
        if not logistics:
            return None
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Logistics WHERE id=?', (logistics_id,))
        conn.commit()
        conn.close()
        return logistics

    def get_category(self, category_id):
        return self.category_repo.get_by_id(category_id)
