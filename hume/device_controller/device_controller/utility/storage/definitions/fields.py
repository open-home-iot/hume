PRIMARY_KEY = 1


class ForeignKey:

    def __init__(self, cls, primary_key=True):
        self._key = cls
        self._is_primary_key = primary_key

    @property
    def key(self):
        return self._key

    @property
    def is_primary_key(self):
        return self._is_primary_key
