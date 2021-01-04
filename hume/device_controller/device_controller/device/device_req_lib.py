import logging
import requests

from device_controller.util.args import get_arg, DEVICE_MOCK_ADDRESS


LOGGER = logging.getLogger(__name__)


"""
This module provides functions for sending requests to a device.
"""


def _device_url(device):
    """
    Returns a URL to the parameter device, ended with a '/'.

    :type device: Device
    """
    mock_address = get_arg(DEVICE_MOCK_ADDRESS)

    if mock_address:
        return mock_address + "/"

    return f"http://{device.ip_address}:32222/"


def capability_request(device):
    """
    Sends a capability request to the parameter device, expecting information
    about the device as a response.

    :type device: Device
    :returns: None or device capabilities as a dictionary
    """
    # Possible response:
    # {
    # 	  "uuid": "e2bf93b6-9b5d-4944-a863-611b6b6600e7",
    #     "name": "THERMO X2",
    #     "description": "Combined Thermometer and Humidity sensor.",
    #     "category": 0,
    #     "type": 0,
    #     "data_groups": [
    #         {
    #             "id": 0,
    #             "name": "Temperature"
    #         },
    #         {
    #             "id": 1,
    #             "name": "Humidity"
    #         }
    #     ],
    #     "actions": [
    #         {
    #             "id": 0,
    #             "name": "Read temperature",
    #             "type": 1,
    #             "return_type": 1,
    #             "data_group": 0
    #         },
    #         {
    #             "id": 1,
    #             "name": "Read humidity",
    #             "type": 1,
    #             "return_type": 1,
    #             "data_group": 1
    #         }
    #     ]
    # }
    response = requests.get(_device_url(device) + "capabilities")

    if response.status_code == 200:
        return response.json()

    return None
