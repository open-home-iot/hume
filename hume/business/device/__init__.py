from . import application


def start(utility_applications=None, transport_applications=None):
    device_application = application.DeviceApplication()
    device_application.start(
        utility_applications=utility_applications,
        transport_applications=transport_applications
    )

    return device_application
