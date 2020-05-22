import peewee

from datetime import datetime

from device_controller.util.storage import PersistentModel


class Device(PersistentModel):

    uuid = peewee.CharField()
    ip_address = peewee.CharField()


class DeviceStatus:

    key: int  # Device ID

    heartbeat: datetime
    state: str

    def __init__(self, key, heartbeat=None, state=None):
        self.key = key
        self.heartbeat = heartbeat
        self.state = state
