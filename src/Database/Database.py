import sqlite3
from sqlite3 import Error
from pathlib import Path

from .DatabaseExceptions import UniqueConstraintFailedException


class Database:

    def __init__(self, db_path: str = "../data.db"):
        self.db_path = Path(db_path).resolve()
        self.last_id = None

    def _connect(self):
        try:
            connection = sqlite3.connect(self.db_path.as_posix())
            return connection
        except Error as e:
            print(f"[Database] Connection error: {e}")
            raise

    def execute_query(self, query, *params):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                # Flatten params if a single list or tuple was passed
                if len(params) == 1 and isinstance(params[0], (list, tuple)):
                    cursor.execute(query, params[0])
                else:
                    cursor.execute(query, params)
                conn.commit()
                self.last_id = cursor.lastrowid
                print("Query executed successfully")
        except Error as e:
            if hasattr(e, "sqlite_errorcode") and e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                # Unique constraint failed
                raise UniqueConstraintFailedException(query, params)
            print(f"[Database] Error: {e}")
            raise

    def execute_read_query(self, query, *params):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                # Flatten params if a single list or tuple was passed
                if len(params) == 1 and isinstance(params[0], (list, tuple)):
                    cursor.execute(query, params[0])
                else:
                    cursor.execute(query, params)
                rows = cursor.fetchall()
                return rows
        except Error as e:
            print(f"[Database] Read error: {e}")
            raise

    def get_last_id(self):
        return self.last_id


if __name__ == "__main__":
    db = Database()

