from . import application


def start(utility_applications=None, transport_applications=None):
    hint_application = application.HintApplication()
    hint_application.start(
        utility_applications=utility_applications,
        transport_applications=transport_applications
    )

    return hint_application
