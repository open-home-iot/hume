import logging
from abc import ABC

from device_controller.utility.storage.definitions import SUPPORTED_FIELDS, \
    is_key


LOGGER = logging.getLogger(__name__)


class DataModel(ABC):
    """
    Base class for data models for an application.

    While statically defined, it will be used to register new data models.

    Instantiated data models are intended to serve as an interface towards
    the data store for application where they can instantiate new DataModel()
    instances, tweak the data and call the data store's API to save the
    current object state. Saving the object state should then either store a
    new instance or override an old one, both locally and persistently (if
    the model has 'persistent' set to True).
    """

    persistent = True
    _key: str = None

    def __init__(self, **kwargs):
        """
        __init__ is provided in order for inheriting classes to define a
        'create' method which instantiates the data model. The create method
        shall accept kwargs for each of the model's fields that the user wants
        to set on the model instance. __init__ here then applies those kwargs
        to each corresponding model field.

        Reserved field names are, do NOT override them:
         * persistent
         * _key

        :param kwargs: .
        """
        for key, val in kwargs.items():
            self.__setattr__(key, val)

    def key(self):
        """
        Returns the field name of the model's key.

        :return: string of the model's key field name
        """
        if self._key:
            return self._key

        key_count = 0
        fields = vars(self.__class__)
        for k, v in fields.items():
            if is_key(v):
                key_count += 1
                self._key = k

        if key_count == 1:
            return self._key

        LOGGER.debug(f"Key was: {self._key}")

        raise KeyError("Make sure there is exactly one key for the model: {}"
                       .format(self.__class__.__name__))

    def get_model_fields(self):
        """
        Gets all of the model's field names as a list. Will filter our all
        unsupported fields. Supported fields are all those fields as defined in
        storage.definitions.fields

        :return: list of the model's field names
        """
        LOGGER.debug(f"Getting model fields")

        fields = vars(self.__class__)

        filtered_fields = [(key, value) for key, value in fields.items()
                           if value.__class__.__name__ in SUPPORTED_FIELDS]

        return filtered_fields
