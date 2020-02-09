from device_controller.utility.storage.definitions import DataModel, \
    ForeignKey, Schedule, PRIMARY_KEY

from device_controller.device.model import Device, DeviceAction


class DeviceConfiguration(DataModel):

    id = int(PRIMARY_KEY)
    # One device could have many configurations
    device = ForeignKey(Device, primary_key=False)  # May not be unique if multiple configurations

    # Timing, perform action every X seconds/minutes...
    interval = int()

    # Follows the schedule pattern, adds ability to set weekdays
    schedule = Schedule()

    # Trigger -> perform action
    # Is this supposed to be a foreign key?
    trigger_device = ForeignKey(Device, primary_key=False)  # Device to watch, cannot be self
    trigger_string = str()  # Trigger level to watch for, must be some sort of pattern
    trigger_action = ForeignKey(DeviceAction, primary_key=False)  # Must be own device action!

    def local(self):
        return ()

    def persistent(self):
        return self.device, self.interval, self.schedule, self.trigger_device, \
               self.trigger_string, self.trigger_action,
