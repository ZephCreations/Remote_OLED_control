import sqlite3
from sqlite3 import Error

from DatabaseExceptions import UniqueConstraintFailedException


class Database:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            # Create database connection
            cls._connection = cls._create_connection()
            print("=============Created=============")
        return cls._instance


    @classmethod
    def _create_connection(cls):
        connection = None
        try:
            connection = sqlite3.connect("../data.db")
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection


    def __init__(self):
        self.last_id = self._connection.cursor().lastrowid


    def get_connection(self):
        return self.__class__._connection

    def execute_query(self, query, *params):
        cursor = self._connection.cursor()
        try:
            cursor.execute(query, params)
            self.last_id = cursor.lastrowid
            self._connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_read_query(self, query, *params):
        cursor = self._connection.cursor()
        result = None
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def get_last_id(self):
        return self.last_id

    def __del__(self):
        # On object deletion, release database
        self._connection.close()


if __name__ == "__main__":
    db = Database()

