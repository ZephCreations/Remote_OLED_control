from Database import Database, Display, Profile

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
        return display # return with updated id

    def update_display(self, display: Display):
        query = (
            "UPDATE display_table "
            "SET content = ?, Type_ID = ? "
            "WHERE Profile_ID = ? AND Screen_ID = ?;"
        )
        cursor = self.__connection.execute_query(
            query, display.content, display.type_id,
            display.profile_id, display.screen_id
        )

        # Check if anything was updated
        if cursor and cursor.rowcount == 0:
            print("[DisplayDAO] Warning: No matching display found to update.")

        # Return the updated version from DB
        updated = self.get_display_by_value(
            display.profile_id,
            display.screen_id
        )
        return updated or display

    def remove_display(self, display: Display):
        query = "DELETE FROM display_table WHERE Display_ID = ?;"
        self.__connection.execute_query(query, display.id)

    def get_display(self, display_id: int):
        query = f"SELECT * FROM display_table WHERE Display_ID = ?;"
        rows = self.__connection.execute_read_query(query, display_id)
        return self._to_display(rows[0]) if rows else None

    def get_display_by_value(self, profile_id: int, screen_id: int):
        query = (
            "SELECT * FROM display_table "
            "WHERE Profile_ID = ? AND Screen_ID = ?;"
        )
        rows = self.__connection.execute_read_query(query, profile_id, screen_id)
        return self._to_display(rows[0]) if rows else None

    def get_all(self):
        query = f"SELECT * FROM display_table;"
        rows = self.__connection.execute_read_query(query)
        return [self._to_display(row) for row in rows]

    def get_all_by_profile_id(self, profile: Profile):
        query = f"SELECT * FROM display_table WHERE Profile_ID = ?;"
        rows = self.__connection.execute_read_query(query, profile.id)
        return [self._to_display(row) for row in rows]

    # ----------------------------------------------------
    # Internal helper
    # ----------------------------------------------------
    @staticmethod
    def _to_display(row):
        display = Display(
            profile_id=row[1],
            screen_id=row[2],
            type_id=row[3],
            content=row[4],
        )
        display.id = row[0]
        return display


if __name__ == "__main__":
    displayDAO = DisplayDAO()

    # Test getting single value
    sample_profile = Display(1, 1, 1, "Hello There")

    # Add profile
    displayDAO.add_display(sample_profile)

    # Get profile
    print(displayDAO.get_display(sample_profile.id))
    print(displayDAO.get_all())

    # Remove profile
    displayDAO.remove_display(sample_profile)
    print(displayDAO.get_all())

