from . import application


def start(*args, **kwargs):
    """
    Start method of this application module. When invoked, this function shall
    start the underlying application and return its instance.

    :return: Hint
    """
    hint = application.Hint()
    hint.start(*args, **kwargs)

    return hint
