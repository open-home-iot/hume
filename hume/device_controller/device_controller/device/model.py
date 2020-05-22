import peewee

from datetime import datetime

from device_controller.util.storage import PersistentModel


class Device(PersistentModel):

    parent = peewee.ForeignKeyField('self', related_name="children", null=True)

    uuid = peewee.CharField()
    ip_address = peewee.CharField()

    # This information is not needed by HUME.
    # name = peewee.CharField()
    # cls = peewee.SmallIntegerField()
    # spec = peewee.SmallIntegerField()


class DeviceAction(PersistentModel):

    # This is not the PK!
    device = peewee.ForeignKeyField(Device, backref="device_actions")

    name = peewee.CharField()

    # Depending on the type, expect the accepted_input to be different things,
    # stateful actions have a list of options for instance.
    type = peewee.SmallIntegerField()

    # Either a comma separated list of input or something to indicate the
    # data type, like: int|str|bool etc.
    accepted_input = peewee.CharField()

    return_type = peewee.SmallIntegerField()


class DeviceStatus:

    key: int  # Device ID

    heartbeat: datetime
    state: str

    def __init__(self, key, heartbeat=None, state=None):
        self.key = key
        self.heartbeat = heartbeat
        self.state = state

