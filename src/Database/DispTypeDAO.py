from Database import Database, DispType, DispTypeList, UniqueConstraintFailedException

class DispTypeDAO:

    def __init__(self):
        self.__connection = Database()
        self._make_table()
        self._add_static_values()

    def _add_static_values(self):
        # Loop through Enum
        for disp_type in list(DispTypeList):
            try:
                self.add_type(DispType(disp_type.name))
            except UniqueConstraintFailedException:
                pass


    def _make_table(self):
        query = ("CREATE TABLE IF NOT EXISTS type_table ( "
                 "Type_ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                 "Name TEXT NOT NULL UNIQUE);")
        self.__connection.execute_query(query)

    def add_type(self, disp_type: DispType):
        query = "INSERT INTO type_table (Name) VALUES (?);"
        self.__connection.execute_query(query, disp_type.name)
        disp_type.id = self.__connection.get_last_id()

    def remove_type(self, disp_type: DispType):
        query = "DELETE FROM type_table WHERE Type_ID = ?"
        self.__connection.execute_query(query, disp_type.id)

    def get_type(self, disp_type: DispType):
        query = f"SELECT * FROM type_table WHERE Type_ID = ?"
        return self.__connection.execute_read_query(query, disp_type.id)

    def get_type_by_value(self, name: str):
        query = f"SELECT * FROM type_table WHERE Name = ?"
        return self.__connection.execute_read_query(query, name)

    def get_all(self):
        query = f"SELECT * FROM type_table"
        return self.__connection.execute_read_query(query)

if __name__ == "__main__":
    typeDAO = DispTypeDAO()

    # Test getting single value
    type_enum = DispTypeList.SELECTION
    sample_disp_type = DispType(type_enum.name)
    sample_disp_type.id = type_enum.value

    print(typeDAO.get_type(sample_disp_type))
    print(typeDAO.get_all())
    print(typeDAO.remove_type(sample_disp_type))
    print(typeDAO.get_all())


