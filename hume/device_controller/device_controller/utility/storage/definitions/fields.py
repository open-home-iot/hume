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


class Enum:

    def __init__(self, *options):
        self._options = options

    @property
    def options(self):
        return self._options


class Timestamp:
    pass


class Pattern:

    def __init__(self, pattern):
        self._pattern = pattern

    @property
    def pattern(self):
        return self._pattern


class Schedule:
    pass
