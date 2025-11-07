from Database import Database, Screen


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
        return screen

    def update_screen(self, screen: Screen):
        query = "UPDATE screen_table SET Address = ? WHERE Screen_ID = ?;"
        cursor = self.__connection.execute_query(query, screen.address, screen.id)

        # Check if anything was updated
        if cursor and cursor.rowcount == 0:
            print("[ScreenDAO] Warning: No Matching screen found to update.")

        # Return updated version from DB
        updated = self.get_screen_by_value(screen.address)
        return updated or screen

    def remove_screen(self, screen: Screen):
        query = "DELETE FROM screen_table WHERE Screen_ID = ?"
        self.__connection.execute_query(query, screen.id)

    def get_screen(self, screen: Screen):
        query = f"SELECT * FROM screen_table WHERE Screen_ID = ?"
        rows = self.__connection.execute_read_query(query, screen.id)
        return self._to_screen(rows[0]) if rows else None

    def get_screen_by_value(self, address: int):
        query = f"SELECT * FROM screen_table WHERE Address = ?"
        rows = self.__connection.execute_read_query(query, address)
        return self._to_screen(rows[0]) if rows else None

    def get_all(self):
        query = f"SELECT * FROM screen_table"
        rows = self.__connection.execute_read_query(query)
        return [self._to_screen(row) for row in rows]

    # ----------------------------------------------------
    # Internal helper
    # ----------------------------------------------------
    @staticmethod
    def _to_screen(row):
        screen = Screen(address=row[1]
        )
        screen.id = row[0]
        return screen


if __name__ == "__main__":
    screenDAO = ScreenDAO()

    # Test getting single value
    sample_screen = Screen(0b00100000)

    screenDAO.add_screen(sample_screen)
    print(screenDAO.get_screen(sample_screen))
    print(screenDAO.get_all())
    print(screenDAO.remove_screen(sample_screen))
    print(screenDAO.get_all())


