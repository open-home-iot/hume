import peewee

from datetime import datetime

from device_controller.utility.storage import PersistentModel


class Device(PersistentModel):

    name = peewee.CharField()
    type = peewee.SmallIntegerField()


class DeviceAction(PersistentModel):

    device = peewee.ForeignKeyField(Device, backref="device_actions")

    name = peewee.CharField()
    type = peewee.SmallIntegerField()

    parameter_type = peewee.SmallIntegerField()
    parameter_description = peewee.CharField()

    return_type = peewee.SmallIntegerField()


class DeviceStatus:

    key: int  # Device ID

    heartbeat: datetime
    state: str

    def __init__(self, key, heartbeat=None, state=None):
        self.key = key
        self.heartbeat = heartbeat
        self.state = state

