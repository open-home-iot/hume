from device_controller.util.storage import PersistentModel


# TODO How can we make guards work? It's nice to guard some actions from being
# TODO executed automatically, perhaps from a config interval timing out.
# TODO Have to evaluate usability and have a clear use-case before implementing
# TODO because it will become quite tricky, and should not be done for nothing.

class DeviceConfiguration(PersistentModel):
    # TODO split this up into timers, schedules, and triggers. Keeping
    # TODO everything in the same model is very poorly normalized.
    pass
