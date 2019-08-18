from . import application


def start(args=None):
    """
    Start method of this application module. When invoked, this function shall
    start the underlying application and return its instance.

    :param args: arguments intended for the scheduler application.
    :return: SchedulerApplication
    """
    scheduler_application = application.SchedulerApplication()
    scheduler_application.start(args=args)

    return scheduler_application
