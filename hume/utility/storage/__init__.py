from . import application


def start(args=None):
    """
    Start method of this application module. When invoked, this function shall
    start the underlying application and return its instance.

    :param args: arguments intended for the storage application.
    :return: StorageApplication
    """
    storage_application = application.StorageApplication()
    storage_application.start(args=args)

    return storage_application
