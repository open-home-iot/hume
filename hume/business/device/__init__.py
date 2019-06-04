from . import application


def start():
    device_application = application.DeviceApplication()
    device_application.start()

    return device_application
