from Database import Database
from Display import Display

class DisplayDAO:

    def __init__(self):
        self.__connection = Database()
        self._make_table()

    def _make_table(self):
        query = ("CREATE TABLE IF NOT EXISTS display_table ( "
                 "Display_ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                 "Profile_ID INTEGER NOT NULL, "
                 "Screen_ID INTEGER NOT NULL, "
                 "Type_ID INTEGER NOT NULL, "
                 "content TEXT DEFAULT NULL,"
                 "FOREIGN KEY (Profile_ID) REFERENCES profile_table (Profile_ID) ON UPDATE CASCADE ON DELETE CASCADE, "
                 "FOREIGN KEY (Screen_ID) REFERENCES screen_table (Screen_ID) ON UPDATE CASCADE ON DELETE CASCADE, "
                 "FOREIGN KEY (Type_ID) REFERENCES type_table (Type_ID) ON UPDATE CASCADE ON DELETE CASCADE"
                 ");")
        self.__connection.execute_query(query)

    def add_display(self, display: Display):
        query = "INSERT INTO display_table (Profile_ID, Screen_ID, Type_ID, content) VALUES (?, ?, ?, ?);"
        self.__connection.execute_query(query, display.profile_id, display.screen_id, display.type_id, display.content)
        display.id = self.__connection.get_last_id()

    def remove_display(self, display: Display):
        query = "DELETE FROM display_table WHERE Display_ID = ?"
        self.__connection.execute_query(query, display.id)

    def get_display(self, display: Display):
        query = f"SELECT * FROM display_table WHERE Display_ID = ?"
        return self.__connection.execute_read_query(query, display.id)

    def get_all(self):
        query = f"SELECT * FROM display_table"
        return self.__connection.execute_read_query(query)


if __name__ == "__main__":
    displayDAO = DisplayDAO()

    # Test getting single value
    sample_profile = Display(1, 1, 1, "Hello There")

    # Add profile
    displayDAO.add_display(sample_profile)

    # Get profile
    print(displayDAO.get_display(sample_profile))
    print(displayDAO.get_all())

    # Remove profile
    displayDAO.remove_display(sample_profile)
    print(displayDAO.get_all())

