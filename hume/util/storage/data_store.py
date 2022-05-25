import logging
from typing import Type, TypeVar

from util.storage.local_storage import LocalStorage
from util.storage.persistent_storage import PersistentStorage
from util.storage.defs import Model


LOGGER = logging.getLogger(__name__)

ModelInstance = TypeVar("ModelInstance")


class DataStore:
    """
    Class that handles storage for the HUME services. It has both local and
    persistent storage capabilities. Local does not survive reboots, persisted
    data does.
    """

    def __init__(self):
        self._persistent_storage: PersistentStorage = PersistentStorage()
        self._local_storage: LocalStorage = LocalStorage()

    def register(self, model: Type[Model]):
        """
        Register models with the DataStore, which allocates storage space for
        model instances.
        """
        # Registration process:
        # 1. Define storage space in _store, named same as model class
        # 2. Get data from storage if persistent
        LOGGER.info(f"registering model: {model.__name__}")

        if model.persistent:
            self._persistent_storage.define_storage(model)
        self._local_storage.define_storage(model)

        if model.persistent:
            model_instances = self._persistent_storage.get_all(model)

            for instance in model_instances:
                self._local_storage.set(instance)

    def set(self, instance: Model):
        """
        Stores an object in the data store.
        """
        LOGGER.debug(f"set {instance}")
        self._persistent_storage.set(instance)
        self._local_storage.set(instance)

    def get(self, model: Type[Model], key: str) -> ModelInstance:
        """
        Get a single object matching the provided key. Will always check local
        storage only as it should be up-to-date with persistent storage.
        """
        LOGGER.debug(f"get {model.__name__}:{key}")
        return self._local_storage.get(model, key)

    def get_all(self, model: Type[Model]) -> [ModelInstance]:
        """
        Get all instances of a model.
        """
        LOGGER.debug(f"get all {model.__name__}")
        return self._local_storage.get_all(model)

    def delete(self, instance: Model):
        """Delete a model instance."""
        LOGGER.debug(f"delete {instance}")
        self._persistent_storage.delete(instance)
        self._local_storage.delete(instance)

    def delete_all(self, model=None):
        """Flush all local and persistent data."""
        LOGGER.debug(f"delete all, model={model}")
        self._persistent_storage.delete_all(model=model)
        self._local_storage.delete_all(model=model)

    """
    Private
    """
