import peewee

from storage import PersistentModel
from storage.definitions import SINGLETON


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


class HintAuthentication:

    def __init__(self, session_id):
        """
        :param session_id: Django session ID used to authenticate consecutive
                           requests
        """
        self.session_id = session_id

    @staticmethod
    def local_key_field():
        return SINGLETON
