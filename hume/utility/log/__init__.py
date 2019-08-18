from . import application


def start(args=None):
    """
    Start method of this application module. When invoked, this function shall
    start the underlying application and return its instance.

    :param args: arguments intended for the log application.
    :return: LogApplication
    """
    log_application = application.LogApplication()
    log_application.start(args=args)

    return log_application
