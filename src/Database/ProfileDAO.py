from Database import Database, Profile


class ProfileDAO:

    def __init__(self):
        self.__connection = Database()
        self._make_table()

    def _make_table(self):
        query = ("CREATE TABLE IF NOT EXISTS profile_table ( "
                 "Profile_ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                 "Name TEXT NOT NULL UNIQUE);")
        self.__connection.execute_query(query)

    def add_profile(self, profile: Profile):
        query = "INSERT INTO profile_table (Name) VALUES (?);"
        self.__connection.execute_query(query, profile.name)
        profile.id = self.__connection.get_last_id()
        return profile # return with updated id

    def update_profile(self, profile: Profile):
        query = "UPDATE profile_table SET Name = ? WHERE Profile_ID = ?;"
        cursor = self.__connection.execute_query(query, profile.name, profile.id)
        # Check if anything was updated
        if cursor and cursor.rowcount == 0:
            print("[ProfileDAO] Warning: No matching profile found to update.")

        # Return the updated version from DB
        updated = self.get_profile_by_value(profile.name)
        return updated or profile

    def remove_profile(self, profile: Profile):
        query = "DELETE FROM profile_table WHERE Profile_ID = ?;"
        self.__connection.execute_query(query, profile.id)

    def get_profile(self, profile: Profile):
        query = f"SELECT * FROM profile_table WHERE Profile_ID = ?;"
        rows = self.__connection.execute_read_query(query, profile.id)
        return self._to_profile(rows[0]) if rows else None

    def get_profile_by_value(self, name: str):
        query = f"SELECT * FROM profile_table WHERE Name = ?;"
        rows = self.__connection.execute_read_query(query, name)
        return self._to_profile(rows[0]) if rows else None

    def get_all(self):
        query = f"SELECT * FROM profile_table;"
        rows = self.__connection.execute_read_query(query)
        return [self._to_profile(row) for row in rows]

    # ----------------------------------------------------
    # Internal helper
    # ----------------------------------------------------
    @staticmethod
    def _to_profile(row):
        profile = Profile(name=row[1])
        profile.id = row[0]
        return profile


if __name__ == "__main__":
    profileDAO = ProfileDAO()

    # Test getting single value
    sample_profile = Profile("Default")

    # Add profile
    profileDAO.add_profile(sample_profile)

    # Get profile
    print(profileDAO.get_profile(sample_profile))
    print(profileDAO.get_all())

    # Remove profile
    profileDAO.remove_profile(sample_profile)
    print(profileDAO.get_all())

