from . import application


def start():
    hint_application = application.HintApplication()
    hint_application.start()

    return hint_application
