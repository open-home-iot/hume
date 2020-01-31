from queue import Queue


class ProcedureHandler:

    _queued = Queue()
    _ongoing = list()

    def __init__(self):
        pass
