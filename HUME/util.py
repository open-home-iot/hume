import threading


def async_callback(target=None, callback=None):
    daemon = threading.Thread(daemon=True, target=run, kwargs={'target': target, 'callback': callback})
    daemon.start()


def run(target=None, callback=None):
    res = target()
    callback(res)
