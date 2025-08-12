import sqlite3
from sqlite3 import Error


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
        pass


    def get_connection(self):
        return self.__class__._connection

    def execute_query(self, query):
        cursor = self._connection.cursor()
        try:
            cursor.execute(query)
            self._connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_read_query(self, query):
        cursor = self._connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")


if __name__ == "__main__":
    db = Database()

