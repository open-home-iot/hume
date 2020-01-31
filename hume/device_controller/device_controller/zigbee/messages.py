class BaseDeviceProperties:
    id: int


# IN
class ZBIn:

    class DeviceCapabilities(BaseDeviceProperties):
        pass

    class DeviceEvent(BaseDeviceProperties):
        pass

    class DeviceHeartbeat(BaseDeviceProperties):
        pass

    class DeviceActionResponse(BaseDeviceProperties):
        pass


# OUT
class ZBOut:

    class DeviceAction(BaseDeviceProperties):
        pass

    class DeviceHeartbeat(BaseDeviceProperties):
        pass
