import sqlite3
import threading

class ORM:
    def __init__(self, db_path='database.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.lock = threading.Lock()

    def execute(self, query, params=(), commit=False):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            if commit:
                self.conn.commit()
            return cursor

    def fetchall(self, query, params=()):
        cursor = self.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def fetchone(self, query, params=()):
        cursor = self.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def close(self):
        self.conn.close()
