import peewee

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


class DeviceState:

    device = peewee.ForeignKeyField(Device)

    state = peewee.CharField


class DeviceStatus:

    device = peewee.ForeignKeyField(Device)

    heartbeat = peewee.TimestampField()
