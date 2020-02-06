from device_controller.utility.storage.definitions import DataModel


class DeviceConfiguration(DataModel):

    device_id = int()

    # Timing
    interval = int()

    def local(self):
        pass

    def persistent(self):
        return self.device_id,
