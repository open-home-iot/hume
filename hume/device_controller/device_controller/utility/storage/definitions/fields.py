import inspect
import sys


class PrimaryKey:
    pass


class ForeignKey:

    def __init__(self, cls, primary_key=True):
        self._cls = cls
        self._is_primary_key = primary_key

    @property
    def cls(self):
        return self._cls

    @property
    def is_primary_key(self):
        return self._is_primary_key


class OneToOne:

    def __init__(self, cls):
        self._cls = cls

    @property
    def cls(self):
        return self._cls


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


class Integer:
    pass


class ManyToMany:

    def __init__(self, cls):
        self._cls = cls

    @property
    def cls(self):
        return self._cls


SUPPORTED_FIELDS = [name for name, cls in
                    inspect.getmembers(sys.modules[__name__], inspect.isclass)]
print("ACCEPTED FIELDS: %s" % SUPPORTED_FIELDS)
