from . import application


def start():
    scheduler_application = application.SchedulerApplication()
    scheduler_application.start()

    return scheduler_application
