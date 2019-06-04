from . import application


def start():
    storage_application = application.StorageApplication()
    storage_application.start()

    return storage_application
