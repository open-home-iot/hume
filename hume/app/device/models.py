import peewee

from util.storage import PersistentModel

from app.device.defs import DeviceTransport


class Device(PersistentModel):
    uuid = peewee.CharField(unique=True, max_length=36, null=True)

    transport = peewee.CharField(choices=(DeviceTransport.BLE.value,
                                          DeviceTransport.SIM.value))
    address = peewee.CharField(unique=True)

    name = peewee.CharField(max_length=255)
    attached = peewee.BooleanField(default=False)

    @staticmethod
    def local_key_field():
        """
        :return: name of local dict key field
        """
        return "uuid"


class DeviceHealth:

    def __init__(self, uuid, heartbeat):
        """
        :param uuid: device UUID
        :param heartbeat: datetime
        """
        self.uuid = uuid
        self.heartbeat = heartbeat

    @staticmethod
    def local_key_field():
        return "uuid"
