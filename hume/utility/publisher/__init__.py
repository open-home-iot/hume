from . import application


def start():
    broker_application = application.PublisherApplication()
    broker_application.start()

    return broker_application
