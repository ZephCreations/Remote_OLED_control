from enum import Enum, verify, UNIQUE, CONTINUOUS


@verify(UNIQUE, CONTINUOUS)
class DispTypeList(Enum):
    TEXT = 1
    TIMER = 2
    IMAGE = 3
    SELECTION = 4


class DispType:

    def __init__(self, name: str):
        self.id = 0
        self.name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value.upper()

