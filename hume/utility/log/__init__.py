from . import application


def start():
    log_application = application.LogApplication()
    log_application.start()

    return log_application
