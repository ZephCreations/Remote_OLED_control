from Database import Database
from Screen import Screen


class ScreenDAO:

    def __init__(self):
        self.__connection = Database()
        self._make_table()

    def _make_table(self):
        query = ("CREATE TABLE IF NOT EXISTS screen_table ( "
                 "Screen_ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                 "Address INT NOT NULL UNIQUE);")
        self.__connection.execute_query(query)

    def add_screen(self, screen: Screen):
        query = "INSERT INTO screen_table (Address) VALUES (?);"
        self.__connection.execute_query(query, screen.address)
        screen.id = self.__connection.get_last_id()

    def remove_screen(self, screen: Screen):
        query = "DELETE FROM screen_table WHERE Screen_ID = ?"
        self.__connection.execute_query(query, screen.id)

    def get_screen(self, screen: Screen):
        query = f"SELECT * FROM screen_table WHERE Screen_ID = ?"
        return self.__connection.execute_read_query(query, screen.id)

    def get_all(self):
        query = f"SELECT * FROM screen_table"
        return self.__connection.execute_read_query(query)

if __name__ == "__main__":
    screenDAO = ScreenDAO()

    # Test getting single value
    sample_screen = Screen(0b00100000)

    screenDAO.add_screen(sample_screen)
    print(screenDAO.get_screen(sample_screen))
    print(screenDAO.get_all())
    print(screenDAO.remove_screen(sample_screen))
    print(screenDAO.get_all())


