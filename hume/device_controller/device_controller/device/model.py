from device_controller.utility.storage.definitions import DataModel, \
    PRIMARY_KEY, ForeignKey, Enum


class Device(DataModel):

    id = int(PRIMARY_KEY)
    name = str()

    def local(self):
        pass

    def persistent(self):
        return self.id, self.name,


class DeviceAction(DataModel):

    id = int(PRIMARY_KEY)
    device = ForeignKey(Device, primary_key=False)

    name = str()

    parameter = bool()
    parameter_type = Enum()
    parameter_description = str()

    def local(self):
        pass

    def persistent(self):
        return self.id, self.device,


class DeviceState(DataModel):

    id = ForeignKey(Device)

    def local(self):
        pass

    def persistent(self):
        pass
