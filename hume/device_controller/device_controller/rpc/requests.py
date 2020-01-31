class BaseDeviceProperties:
    id: int


# IN
class RPCIn:

    class DeviceAttach(BaseDeviceProperties):
        pass

    class DeviceAction(BaseDeviceProperties):
        pass

    class DeviceConfiguration(BaseDeviceProperties):
        pass


# OUT
class RPCOut:
    pass  # Any at all?
