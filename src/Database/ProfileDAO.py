from Database import Database
from Profile import Profile


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

    def remove_profile(self, profile: Profile):
        query = "DELETE FROM profile_table WHERE Profile_ID = ?"
        self.__connection.execute_query(query, profile.id)

    def get_profile(self, profile: Profile):
        query = f"SELECT * FROM profile_table WHERE Profile_ID = ?"
        return self.__connection.execute_read_query(query, profile.id)

    def get_all(self):
        query = f"SELECT * FROM profile_table"
        return self.__connection.execute_read_query(query)


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

