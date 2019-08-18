from . import application


def start(args=None, utility_applications=None, transport_applications=None):
    """
    Start method of this application module. When invoked, this function shall
    start the underlying application and return its instance.

    :param args: arguments intended for the hint application.
    :param utility_applications:   a list of all utility applications that
                                   the hint application is allowed to
                                   use.
    :param transport_applications: a list of all transport applications that
                                   the hint application is allowed to
                                   use.
    :return: HintApplication
    """
    hint_application = application.HintApplication()
    hint_application.start(
        args=args,
        utility_applications=utility_applications,
        transport_applications=transport_applications
    )

    return hint_application
