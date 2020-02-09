from device_controller.utility.storage.definitions import DataModel, \
    ForeignKey, Schedule

from device_controller.device.model import Device, DeviceAction


class DeviceConfiguration(DataModel):

    device = ForeignKey(Device)

    # Timing, perform action every X seconds/minutes...
    interval = int()

    # Follows the schedule pattern, adds ability to set weekdays
    schedule = Schedule()

    # Triggers, perform action
    trigger_device = ForeignKey(Device)  # Device to watch, cannot be self
    trigger_string = str()
    trigger_action = ForeignKey(DeviceAction)

    def local(self):
        pass

    def persistent(self):
        return self.device, self.interval, self.schedule, self.trigger_device, \
               self.trigger_string, self.trigger_action
