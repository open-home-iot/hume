from . import application


def start(args=None):
    """
    Start method of this application module. When invoked, this function shall
    start the underlying application and return its instance.

    :param args: arguments intended for the broker application.
    :return: BrokerApplication
    """
    broker = application.Broker()
    broker.start(args=args)

    return broker
