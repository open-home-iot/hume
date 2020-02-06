from device_controller.utility.storage.definitions import DataModel


class DeviceConfiguration(DataModel):

    id = int()

    def local(self):
        pass

    def persistent(self):
        return self.id,
