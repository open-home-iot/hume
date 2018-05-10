import unittest

from unittest.mock import Mock

from serial_interface import serial_interface


class SerialInterfaceTests(unittest.TestCase):

    # SET UP / TEAR DOWN

    @classmethod
    def setUpClass(cls):
        serial_port = Mock()
        serial_interface.CONNECTION = serial_port

    # SET UP / TEAR DOWN

    def test_error(self):
        serial_interface.serial_port.readline = Mock(return_value="9".encode('utf-8'))

        serial_interface.read_incoming_data()
