import logging

"""Fields for internal data models"""

LOGGER = logging.getLogger(__name__)


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


class Timestamp:
    pass


class Schedule:
    pass


class String:
    pass


class Integer:
    pass


def has_relation(field):
    """
    Check for if a field has any relations.

    :param field: .
    :return: True | False
    """
    return isinstance(field, ForeignKey)


def is_key(field):
    """
    Check if a field is the key of a model.

    :param field: .
    :return: True | False
    """
    if isinstance(field, PrimaryKey):
        return True
    elif isinstance(field, ForeignKey):
        return field.is_primary_key
    else:
        return False
