

class UniqueConstraintFailedException(Exception):
    def __init__(self, query, values, msg="Unique constraint failed"):
        self.query = query
        self.values = values
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return (f"{self.msg}: \n"
                f"Query -> {self.query}\n"
                f"Values -> {self.values}")