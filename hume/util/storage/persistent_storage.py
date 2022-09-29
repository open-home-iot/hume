import copy
import logging
import redis

from typing import Type, Mapping, Union

from util.storage.defs import Model, model_error, SINGLETON

LOGGER = logging.getLogger(__name__)
ENCODABLE_TYPES = [int, str, float, bytes]


class PersistentStorage:
    """
    Handles caching persistent storage items and interactions with Postgres
    through the peewee ORM.
    """

    def __init__(self):
        self._models: [Type[Model]] = []
        self._redis = redis.Redis(host="localhost", port=6379, db=0)

    def define_storage(self, model: Type[Model]):
        """
        Pretty much just keeps track of which models exist to be able to clean
        up after them using delete_all.
        """
        LOGGER.debug("added model to list of models")

        if model in self._models:
            model_error(
                model.__name__,
                custom_message=f"model {model.__name__} is already registered"
            )

        self._models.append(model)

    def set(self, instance: Model):
        """
        Save an object persistently.
        """
        LOGGER.debug("saving in Redis")

        hash_name = PersistentStorage._gen_hash_name(instance)

        # copy to avoid changing the instance __dict__ when preparing for
        # storage
        data = copy.copy(vars(instance))
        data.pop(instance.key) if instance.key != SINGLETON else ...
        for key, value in data.items():
            # do not try to persist None values
            if value is not None:
                self._redis.hset(hash_name,
                                 key,
                                 PersistentStorage._encode_value(value))

    def get_all(self, model: Type[Model]) -> [Model]:
        """
        Get all data associated with the model class cls.
        """
        LOGGER.debug("getting all records from Redis")

        instances = []
        if model.key == SINGLETON:
            hash_name = f"{model.__name__}:{SINGLETON}"
            redis_hash = self._redis.hgetall(hash_name)
            if redis_hash:  # not just an empty dict
                instances.append(PersistentStorage._decode(
                    model, SINGLETON, redis_hash)
                )
                return instances

        for hash_name in self._redis.scan_iter(match=f"{model.__name__}:*"):
            instances.append(PersistentStorage._decode(
                model,
                # b"ModelName:key" -> key
                hash_name.decode().split(":")[1],
                self._redis.hgetall(hash_name))
            )
        return instances

    def delete(self, instance: Model):
        """Delete the input instance from Redis."""
        LOGGER.debug("delete in Redis")

        self._redis.delete(PersistentStorage._gen_hash_name(instance))

    def delete_all(self, model=None):
        """Delete all data stored in Redis."""
        LOGGER.debug("delete all in Redis")

        if model is not None:
            for hash_name in self._redis.scan_iter(
                    match=f"{model.__name__}:*"):
                self._redis.delete(hash_name)
            return

        for registered_model in self._models:
            for hash_name in self._redis.scan_iter(
                    match=f"{registered_model.__name__}:*"):
                self._redis.delete(hash_name)

    """
    Private
    """

    @staticmethod
    def _encode_value(value: Union[bool, str, int, float, bytes]) -> \
            Union[str, int, float, bytes]:
        if type(value) in ENCODABLE_TYPES:
            return value
        elif type(value) is bool:
            return int(value)
        else:
            LOGGER.error(f"got unexpected type {type(value)}")
        # add more expected types as needed

    @staticmethod
    def _decode(model: Type[Model],
                key: str,
                redis_hash: Mapping[bytes, bytes]) -> Model:
        kwargs = {model.key: key} if key != SINGLETON else {}
        kwargs.update({key.decode(): value.decode()
                       for key, value in redis_hash.items()})
        return model.decode(**kwargs)

    @staticmethod
    def _gen_hash_name(instance: Model) -> str:
        """
        Generate the hash name to be used towards Redis for a given instance
        of a model.
        """
        hash_name = (f"{instance.__class__.__name__}:"
                     f"{PersistentStorage._gen_key(instance)}")
        return hash_name

    @staticmethod
    def _gen_key(instance: Model) -> str:
        return (getattr(instance, instance.key)
                if instance.key != SINGLETON else SINGLETON)
