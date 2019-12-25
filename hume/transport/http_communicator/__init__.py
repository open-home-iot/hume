from . import application


def start(args=None, utility_applications=None):
    """
    Start method of this application module. When invoked, this function shall
    start the underlying application and return its instance.

    :param args: arguments intended for the application.
    :param utility_applications: a dict of all utility applications that
                                 the application is allowed to
                                 use.
    :return: HttpCommunicator
    """
    http_communicator = application.HttpCommunicator()
    http_communicator.start(
        args=args,
        utility_applications=utility_applications
    )

    return http_communicator
