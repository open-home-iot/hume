from . import application


def start():
    http_application = application.HttpApplication()
    http_application.start()

    return http_application
