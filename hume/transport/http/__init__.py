from . import application


def start(args=None, utility_applications=None):
    """
    Start method of this application module. When invoked, this function shall
    start the underlying application and return its instance.

    :param args: arguments intended for the http application.
    :param utility_applications: a list of all utility applications that
                                 the http application is allowed to
                                 use.
    :return: HttpApplication
    """
    http_application = application.HttpApplication()
    http_application.start(
        args=args,
        utility_applications=utility_applications
    )

    return http_application
