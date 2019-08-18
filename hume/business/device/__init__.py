from . import application


def start(args=None, utility_applications=None, transport_applications=None):
    """
    Start method of this application module. When invoked, this function shall
    start the underlying application and return its instance.

    :param args: arguments intended for the device application.
    :param utility_applications:   a list of all utility applications that
                                   the device application is allowed to
                                   use.
    :param transport_applications: a list of all transport applications that
                                   the device application is allowed to
                                   use.
    :return: DeviceApplication
    """
    device_application = application.DeviceApplication()
    device_application.start(
        args=args,
        utility_applications=utility_applications,
        transport_applications=transport_applications
    )

    return device_application
