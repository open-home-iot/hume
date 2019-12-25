from . import application


def start(args=None, utility_applications=None):
    """
    Start method of this application module. When invoked, this function shall
    start the underlying application and return its instance.

    :param args: arguments intended for the serial_listener application.
    :param utility_applications: a dict of all utility applications that
                                 the serial_listener application is allowed to
                                 use.
    :return: SerialApplication
    """
    serial_communicator = application.SerialCommunicator()
    serial_communicator.start(
        args=args,
        utility_applications=utility_applications
    )

    return serial_communicator
