from . import application


def start():
    serial_application = application.SerialApplication()
    serial_application.start()

    return serial_application
