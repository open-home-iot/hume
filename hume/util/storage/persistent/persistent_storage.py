import logging

from .postgres import PostgresProxy


LOGGER = logging.getLogger(__name__)


class PersistentStorage:
    """
    Handles caching persistent storage items and interactions with Postgres
    through the peewee ORM.
    """

    def __init__(self, user, password):
        self._pg_proxy = PostgresProxy(user, password)
        self._models = []

    def start(self):
        """Starts the connection towards Postgres."""
        LOGGER.info("starting PersistentStorage")

        self._pg_proxy.start()

    def define_storage(self, model):
        """
        Defines cache space and tables in postgres.

        :param model: .
        """
        LOGGER.debug("defining persistent storage")

        self._pg_proxy.define_table(model)
        self._models.append(model)

    @staticmethod
    def save(obj):
        """
        Save an object persistently.

        :param obj: object to save
        """
        LOGGER.debug("saving to database")

        obj.save()

    @staticmethod
    def get_all(cls):
        """
        Get all data associated with the model class cls.

        :param cls: class to get data for
        :return: all data for model class
        """
        LOGGER.debug(f"getting all records for class: {cls}")

        return cls.select()

    @staticmethod
    def delete(obj):
        """
        Removes the object from persistent storage.

        :param obj:
        :return:
        """
        LOGGER.debug(f"delete object: {obj}")

        obj.delete_instance()

    def delete_all(self):
        """
        Drop all tables.
        """
        LOGGER.debug("deleting all persistent data")

        self._pg_proxy.drop_tables(self._models)
