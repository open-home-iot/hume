import peewee

from datetime import datetime

from device_controller.util.storage import PersistentModel


class Device(PersistentModel):

    # HUME only needs connection information for the device, not information
    # about sub-devices (if compound). Sub-device info could be useful for
    # validating incoming requests, but if proper authentication and
    # authorization is in place, each request should anyway come from a solid
    # source with enough knowledge about device structures.
    uuid = peewee.CharField()
    ip_address = peewee.CharField()

    attached = peewee.BooleanField()


# class DeviceStatus:
#
#     key: int  # Device ID
#
#     heartbeat: datetime
#     state: str
#
#     def __init__(self, key, heartbeat=None, state=None):
#         self.key = key
#         self.heartbeat = heartbeat
#         self.state = state
