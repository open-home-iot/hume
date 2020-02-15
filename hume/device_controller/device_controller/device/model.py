from device_controller.utility.storage.definitions import DataModel, \
    ForeignKey, Enum, Timestamp, OneToOne, PrimaryKey, String

ACTUATOR = 0
SENSOR = 1
EVENT = 2
COMBINED = 3

TYPE_INTEGER = 0
TYPE_BOOLEAN = 1
TYPE_STRING = 2
TYPE_NONE = 3

TYPE_ENUM = Enum(TYPE_INTEGER, TYPE_BOOLEAN, TYPE_STRING, TYPE_NONE)


class Device(DataModel):

    id = PrimaryKey()

    name = String()
    type = Enum(ACTUATOR, SENSOR, EVENT, COMBINED)


class DeviceAction(DataModel):

    id = PrimaryKey()
    device = ForeignKey(Device, primary_key=False)

    name = String()
    type = Enum(ACTUATOR, SENSOR)

    parameter_type = TYPE_ENUM
    parameter_description = String()

    return_type = TYPE_ENUM


class DeviceState(DataModel):

    persistent = False

    device = OneToOne(Device)

    state = String()


class DeviceStatus(DataModel):

    persistent = False

    device = OneToOne(Device)

    heartbeat = Timestamp()
