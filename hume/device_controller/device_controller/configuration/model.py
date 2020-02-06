from device_controller.utility.storage.definitions import DataModel, ForeignKey

from device_controller.device.model import Device


class DeviceConfiguration(DataModel):

    device_id = ForeignKey(Device)

    # Timing
    interval = int()

    def local(self):
        pass

    def persistent(self):
        return self.device_id,
