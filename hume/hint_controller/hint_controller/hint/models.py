import peewee

from hume_storage import PersistentModel


class Hume(PersistentModel):

    hume_id = peewee.CharField(max_length=256)
    paired = peewee.BooleanField(default=False)

    @staticmethod
    def local_key_field():
        """
        :return: name of local dict key field
        """
        return "hume_id"


class HumeUser(PersistentModel):

    username = peewee.CharField(max_length=50)
    password = peewee.CharField(max_length=50)

    @staticmethod
    def local_key_field():
        """
        :return: name of local dict key field
        """
        return PersistentModel.SINGLETON
