

class Screen:

    def __init__(self, address):
        self.id = 0
        self.address = address

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

