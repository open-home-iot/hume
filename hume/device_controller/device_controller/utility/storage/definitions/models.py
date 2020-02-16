from abc import ABC

from device_controller.utility.storage.definitions import SUPPORTED_FIELDS, \
    is_key


class DataModel(ABC):

    persistent = True
    _key: str = None

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            self.__setattr__(key, val)

    def key(self):
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

        self._key = None
        raise KeyError("Make sure there is exactly one key for the model: {}"
                       .format(self.__class__.__name__))

    def get_model_fields(self):
        fields = vars(self.__class__)
        #print("model_instance.__class__ vars() result: {}".format(fields))

        filtered_fields = [(key, value) for key, value in fields.items()
                           if value.__class__.__name__ in SUPPORTED_FIELDS]
        #print("filtered out model fields from model_instance.__class__: {}"
        #      .format(filtered_fields))

        return filtered_fields
