from . import application


def start():
    broker_application = application.BrokerApplication()
    broker_application.start()

    return broker_application
