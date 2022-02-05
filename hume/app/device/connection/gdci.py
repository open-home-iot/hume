"""
This module specifies the Generic Device Connection Interface superclass.
"""


import abc

from app.device.models import Device


class GDCI(abc.ABC):

    class Message:
        def __init__(self, content: str):
            self.content = f"^{content}$".encode("utf-8")

    @abc.abstractmethod
    def discover(self, on_devices_discovered) -> None:
        """
        Discover devices in the local network that are not yet connected.

        :param on_devices_discovered: callable([Device]), called when one or
            more devices are found
        """
        pass

    @abc.abstractmethod
    def connect(self, device: Device) -> bool:
        """
        Connect to the given device.

        :returns: True if connected, else False
        """
        pass

    @abc.abstractmethod
    def is_connected(self, device: Device) -> bool:
        """
        Check if a device is connected.

        :returns: True if the device is connected
        """
        pass

    @abc.abstractmethod
    def disconnect(self, device: Device) -> bool:
        """
        Disconnects the given device.

        :returns: True if successful, else False
        """
        pass

    @abc.abstractmethod
    def disconnect_all(self) -> bool:
        """
        Disconnects all devices.

        :returns: True if all devices were successfully disconnected
        """
        pass

    @abc.abstractmethod
    def send(self, msg: Message, device: Device) -> bool:
        """
        Sends the parameter message to the given device.

        :returns: True if successful, else False
        """
        pass

    @abc.abstractmethod
    def notify(self, callback: callable, device: Device):
        """
        Subscribes to messages from the given device, each message will be
        relayed to the parameter callback.

        callback: callable(Device, int, bytearray)
        """
        pass

    @abc.abstractmethod
    def for_each(self, callback: callable):
        """
        Calls input callback for each active connection. The Device instance
        passed to the callback function is bare-bones and only has the
        necessary fields populated to fulfill a call to one of GCI methods.

        callback: callable(Device)
        """
        pass
