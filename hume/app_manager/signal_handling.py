import signal


def bind_signal_handlers(app_manager):
    signal.signal(signal.SIGINT, app_manager.interrupt)
