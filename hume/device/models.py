import peewee

from storage import PersistentModel

from defs import CLI_DEVICE_TRANSPORT_BLE


class Device(PersistentModel):
    transport = peewee.CharField(choices=(CLI_DEVICE_TRANSPORT_BLE,))
    address = peewee.CharField(unique=True)
    name = peewee.CharField(max_length=255)
    uuid = peewee.CharField(unique=True, max_length=36, null=True)
    attached = peewee.BooleanField(default=False)

    @staticmethod
    def local_key_field():
        """
        :return: name of local dict key field
        """
        return "uuid"
