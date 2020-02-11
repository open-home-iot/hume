import inspect
import sys


class PrimaryKey:
    pass


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


class OneToOne:

    def __init__(self, cls):
        self._key = cls

    @property
    def key(self):
        return self._key


class Enum:

    def __init__(self, *options):
        self._options = options

    @property
    def options(self):
        return self._options


class Timestamp:
    pass


class Schedule:
    pass


class String:
    pass


SUPPORTED_FIELDS = [name for name, cls in
                    inspect.getmembers(sys.modules[__name__], inspect.isclass)]
print("ACCEPTED FIELDS: %s" % SUPPORTED_FIELDS)
