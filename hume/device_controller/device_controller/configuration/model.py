import peewee

from device_controller.device.model import Device, DeviceAction
from device_controller.utility.storage import PersistentModel


# TODO How can we make guards work? It's nice to guard some actions from being
# TODO executed automatically, perhaps from a configuration interval timing out.
# TODO Have to evaluate usability and have a clear use-case before implementing
# TODO because it will become quite tricky, and should not be done for nothing.

class DeviceConfiguration(PersistentModel):

    # The action tied to this configuration
    action = peewee.ForeignKeyField(DeviceAction,
                                    backref="device_configurations")

    # Perform 'action' at set interval/schedule
    interval = peewee.IntegerField()
    schedule = peewee.CharField()  # Custom

    # Perform 'action' when...
    watch_device = peewee.ForeignKeyField(Device,
                                          backref="device_configurations")

    # Events and sensors
    on_state = peewee.CharField()

    # Actuators
    on_action = peewee.ForeignKeyField(DeviceAction,
                                       backref="device_configurations")
    on_action_state = peewee.CharField
