import logging

from .postgres import PostgresProxy


LOGGER = logging.getLogger(__name__)


class PersistentStorage:
    """
    Handles caching persistent storage items and interactions with Postgres
    through the peewee ORM.
    """

    def __init__(self):
        """"""
        LOGGER.debug("PersistentStorage __init__")

        self._pg_proxy = PostgresProxy()

    def define_storage(self, model):
        """
        Defines cache space and tables in postgres.

        :param model: .
        """
        LOGGER.debug("Defining persistent storage")

        self._pg_proxy.define_table(model)

    def save(self, obj):
        """
        Save an object persistently.

        :param obj: object to save
        """
        LOGGER.debug("saving to database")

        obj.save()

    def get_all(self, cls):
        """
        Get all data associated with the model class cls.

        :param cls: class to get data for
        :return: all data for model class
        """
        LOGGER.debug(f"getting all records for class: {cls}")

        return cls.select()

    def delete(self, obj):
        """
        Removes the object from persistent storage.

        :param obj:
        :return:
        """
        LOGGER.debug(f"delete object: {obj}")

        obj.delete_instance()
