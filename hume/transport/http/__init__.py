from . import application


def start(utility_applications=None):
    http_application = application.HttpApplication()
    http_application.start(
        utility_applications=utility_applications
    )

    return http_application
