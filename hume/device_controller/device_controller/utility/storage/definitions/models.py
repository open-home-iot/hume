from abc import ABC

from device_controller.utility.storage.definitions import PrimaryKey, \
    ForeignKey, OneToOne, SUPPORTED_FIELDS


class DataModel(ABC):

    persistent = True
    _key: str = None

    singleton = False

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


def is_key(field_value):
    if isinstance(field_value, PrimaryKey):
        return True
    elif isinstance(field_value, ForeignKey):
        return field_value.is_primary_key
    elif isinstance(field_value, OneToOne):
        return True
    else:
        return False
