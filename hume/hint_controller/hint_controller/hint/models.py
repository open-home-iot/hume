import peewee

from hume_storage import PersistentModel
from hume_storage.definitions import SINGLETON


class HumeUser(PersistentModel):

    username = peewee.CharField(max_length=50)
    password = peewee.CharField(max_length=50)

    @staticmethod
    def local_key_field():
        """
        :return: name of local dict key field
        """
        return SINGLETON


class BrokerCredentials(PersistentModel):

    username = peewee.CharField(max_length=50)
    password = peewee.CharField(max_length=50)

    @staticmethod
    def local_key_field():
        return SINGLETON
