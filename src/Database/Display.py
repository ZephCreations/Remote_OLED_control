
class Display:

    def __init__(self, profile_id, screen_id, type_id, content):
        self.id = 0
        self.profile_id = profile_id
        self.screen_id = screen_id
        self.type_id = type_id
        self.content = content

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def profile_id(self):
        return self._profile_id

    @profile_id.setter
    def profile_id(self, value):
        self._profile_id = value

    @property
    def screen_id(self):
        return self._screen_id

    @screen_id.setter
    def screen_id(self, value):
        self._screen_id = value

    @property
    def type_id(self):
        return self._type_id

    @type_id.setter
    def type_id(self, value):
        self._type_id = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

