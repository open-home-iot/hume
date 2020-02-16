import inspect
import sys


class Field:

    _value = None

    @property
    def value(self):
        return self._value


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


def has_relation(field):
    return isinstance(field, ForeignKey) or \
           isinstance(field, OneToOne) or \
           isinstance(field, ManyToMany)


def is_enum(field):
    return isinstance(field, Enum)


def is_key(field):
    if isinstance(field, PrimaryKey):
        return True
    elif isinstance(field, ForeignKey):
        return field.is_primary_key
    elif isinstance(field, OneToOne):
        return True
    else:
        return False
