from . import application


def start(utility_applications=None):
    serial_application = application.SerialApplication()
    serial_application.start(utility_applications=utility_applications)

    return serial_application
