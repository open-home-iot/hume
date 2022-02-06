import logging

import peewee


LOGGER = logging.getLogger(__name__)
PSQL_DB_NAME = "hume"


class PersistentModel(peewee.Model):
    """
    Base class for all persistent models.
    """

    class Meta:
        database = peewee.PostgresqlDatabase(PSQL_DB_NAME)


class PersistentStorage:
    """
    Handles caching persistent storage items and interactions with Postgres
    through the peewee ORM.
    """

    def __init__(self, user, password):
        self._db = peewee.PostgresqlDatabase(PSQL_DB_NAME,
                                             user=user,
                                             password=password)
        self._models = []

    def start(self):
        """Starts the connection towards Postgres."""
        LOGGER.info("starting persistent storage")

    def stop(self):
        """Stops the connection towards Postgres."""
        LOGGER.info("stopping persistent storage")

    def define_storage(self, model):
        """
        Defines cache space and tables in postgres.
        """
        LOGGER.debug("defining persistent storage")
        with self._db as d:
            print(d)
            self._db.create_tables([model])

        self._models.append(model)

    def save(self, obj):
        """
        Save an object persistently.
        """
        LOGGER.debug("saving to database")
        with self._db:
            obj.save()

    def get_all(self, cls):
        """
        Get all data associated with the model class cls.

        :param cls: class to get data for
        :return: all data for model class
        """
        LOGGER.debug(f"getting all records for class: {cls}")
        with self._db:
            return cls.select()

    def delete(self, obj):
        """
        Removes the object from persistent storage.

        :param obj:
        :return:
        """
        LOGGER.debug(f"delete object: {obj}")
        with self._db:
            obj.delete_instance()

    def delete_all(self):
        """
        Drop all tables.
        """
        LOGGER.debug("deleting all persistent data")
        print(self._db.transaction_depth())
        with self._db:
            print(self._db.transaction_depth())
            self._db.drop_tables(self._models)
