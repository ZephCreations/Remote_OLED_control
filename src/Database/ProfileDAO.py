import Database

class ProfileDAO:
    _connection = None

    def __init__(self):
        _connection = Database.SqliteConnection.get_instance()

