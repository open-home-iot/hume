"""
This module specifies the Generic Connection Interface superclass.
"""


import abc

from app.device.models import Device


class GCI(abc.ABC):

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
    def send(self, msg: Message, device: Device) -> bool:
        """
        Sends the parameter message to the given device.

        :returns: True if successful, else False
        """
        pass

    @abc.abstractmethod
    def disconnect(self, device: Device):
        """
        Disconnects the given device.
        """
        pass

    @abc.abstractmethod
    def disconnect_all(self):
        """
        Disconnects all devices.
        """
        pass

    @abc.abstractmethod
    def notify(self, callback, device: Device):
        """
        Subscribes to messages from the given device, each message will be
        relayed to the parameter callback.

        :param callback: callable(Device, int, data)
        :param device: Device
        """
        pass

    @abc.abstractmethod
    def for_each(self, callback: callable):
        """
        Calls input callback for each active connection. The Device instance
        passed to the callback function is bare-bones and only has the
        necessary fields populated to fulfil a call to one of GCI methods.

        :param callback: callable(Device)
        """
        pass