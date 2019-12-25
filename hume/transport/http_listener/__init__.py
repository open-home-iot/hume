from . import application


def start(args=None, utility_applications=None):
    """
    Start method of this application module. When invoked, this function shall
    start the underlying application and return its instance.

    :param args: arguments intended for the application.
    :param utility_applications: a dict of all utility applications that
                                 the application is allowed to
                                 use.
    :return: HttpApplication
    """
    http_listener = application.HttpListener()
    http_listener.start(
        args=args,
        utility_applications=utility_applications
    )

    return http_listener
