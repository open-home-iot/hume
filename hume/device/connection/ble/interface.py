from .application import _conn


def discover(on_devices_discovered=None):
    """
    Discover all nearby BLE devices that comply with the HOME protocal, for BLE
    that means:
    1. Has the NUS service available for UART RX/TX
    2. Has a HOME identifier
    """
    _conn.discover(on_devices_discovered=on_devices_discovered)


def connect():
    pass


def disconnect():
    pass


def send():
    pass


def notify():
    pass
