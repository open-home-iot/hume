from device_controller.utility.storage.definitions import DataModel, \
    PRIMARY_KEY, ForeignKey, Enum, Timestamp


DEVICE_TYPE_ACTUATOR = 0
DEVICE_TYPE_SENSOR = 1
DEVICE_TYPE_COMBINED = 2

DEVICE_ACTION_TYPE_SENSOR = 0
DEVICE_ACTION_TYPE_ACTUATOR = 1

DEVICE_ACTION_PARAMETER_TYPE_INTEGER = 0
DEVICE_ACTION_PARAMETER_TYPE_BOOLEAN = 1
DEVICE_ACTION_PARAMETER_TYPE_STRING = 2
DEVICE_ACTION_PARAMETER_TYPE_NONE = 3


class Device(DataModel):

    id = int(PRIMARY_KEY)
    name = str()
    type = Enum(DEVICE_TYPE_ACTUATOR, DEVICE_TYPE_SENSOR, DEVICE_TYPE_COMBINED)

    def local(self):
        pass

    def persistent(self):
        return self.id, self.name, self.type,


class DeviceAction(DataModel):

    id = int(PRIMARY_KEY)
    device = ForeignKey(Device, primary_key=False)

    name = str()
    type = Enum(DEVICE_ACTION_TYPE_ACTUATOR, DEVICE_ACTION_TYPE_SENSOR)

    parameter_type = Enum(DEVICE_ACTION_PARAMETER_TYPE_INTEGER,
                          DEVICE_ACTION_PARAMETER_TYPE_BOOLEAN,
                          DEVICE_ACTION_PARAMETER_TYPE_STRING,
                          DEVICE_ACTION_PARAMETER_TYPE_NONE)
    parameter_description = str()

    def local(self):
        pass

    def persistent(self):
        return self.id, self.device, self.name, self.type, self.parameter_type,\
               self.parameter_description,


class DeviceState(DataModel):

    device = ForeignKey(Device)

    heartbeat = Timestamp()
    state = str()

    def local(self):
        return self.state

    def persistent(self):
        return self.device, self.heartbeat,
