from device_controller.utility.storage.definitions import DataModel, \
    ForeignKey, Schedule, PrimaryKey, Integer, String

from device_controller.device.model import Device, DeviceAction


# TODO How can we make guards work? It's nice to guard some actions from being
# TODO executed automatically, perhaps from a configuration interval timing out.
# TODO Have to evaluate usability and have a clear use-case before implementing
# TODO because it will become quite tricky, and should not be done for nothing.
#class Guard(DataModel):

    #id = PrimaryKey()

    #device = ForeignKey(Device, primary_key=False)

    #watch_device = ForeignKey(Device, primary_key=False)
    #watch_value = String()


class DeviceConfiguration(DataModel):

    id = PrimaryKey()

    # The action tied to this configuration
    action = ForeignKey(DeviceAction, primary_key=False)

    # Perform 'action' at set interval/schedule
    interval = Integer()
    schedule = Schedule()

    # Perform 'action' when...
    watch_device = ForeignKey(Device, primary_key=False)

    # Events and sensors
    on_state = String()

    # Actuators
    on_action = ForeignKey(DeviceAction, primary_key=False)
    on_action_state = String()

    @classmethod
    def create(cls,
               action,
               interval=None,
               schedule=None,
               watch_device=None,
               on_state=None,
               on_action=None,
               on_action_state=None):
        instance = cls(action=action, interval=interval, schedule=schedule,
                       watch_device=watch_device, on_state=on_state,
                       on_action=on_action, on_action_state=on_action_state)
        return instance
