from Database import Database

class DisplayDAO:

    def __init__(self):
        self.__connection = Database()
        self.make_table()

    def make_table(self):
        query = ("CREATE TABLE IF NOT EXISTS display_table ( "
                 "Display_ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                 "Profile_ID INTEGER NOT NULL, "
                 "Screen_ID INTEGER NOT NULL, "
                 "Type_ID INTEGER NOT NULL, "
                 "content TEXT DEFAULT NULL,"
                 "FOREIGN KEY (Profile_ID) REFERENCES profile_table (Profile_ID) ON UPDATE CASCADE ON DELETE CASCADE, "
                 "FOREIGN KEY (Screen_ID) REFERENCES screens_table (Screen_ID) ON UPDATE CASCADE ON DELETE CASCADE, "
                 "FOREIGN KEY (Type_ID) REFERENCES type_table (Type_ID) ON UPDATE CASCADE ON DELETE CASCADE, "
                 ");")
        self.__connection.execute_query(query)

    def add_display(self):
        pass

    def get_display(self, screen):
        pass


if __name__ == "__main__":
    displayDAO = DisplayDAO()

