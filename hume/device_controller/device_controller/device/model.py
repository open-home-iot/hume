from device_controller.utility.storage.definitions import DataModel, \
    ForeignKey, Enum, Timestamp, OneToOne, PrimaryKey

ACTUATOR = 0
SENSOR = 1
COMBINED = 2

TYPE_INTEGER = 0
TYPE_BOOLEAN = 1
TYPE_STRING = 2
TYPE_NONE = 3

TYPE_ENUM = Enum(TYPE_INTEGER, TYPE_BOOLEAN, TYPE_STRING, TYPE_NONE)


class Device(DataModel):

    id = PrimaryKey()

    name = str()
    type = Enum(ACTUATOR, SENSOR, COMBINED)

    def local(self):
        return ()

    def persistent(self):
        return self.name, self.type,


class DeviceAction(DataModel):

    id = PrimaryKey()
    device = ForeignKey(Device, primary_key=False)

    name = str()
    type = Enum(ACTUATOR, SENSOR)

    parameter_type = TYPE_ENUM
    parameter_description = str()

    return_type = TYPE_ENUM

    def local(self):
        return ()

    def persistent(self):
        return self.device, self.name, self.type, self.parameter_type, \
               self.parameter_description, self.return_type,


class DeviceState(DataModel):

    device = OneToOne(Device)

    heartbeat = Timestamp()
    state = str()

    def local(self):
        return self.heartbeat, self.state,

    def persistent(self):
        return ()
