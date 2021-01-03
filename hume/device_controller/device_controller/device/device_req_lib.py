import logging


LOGGER = logging.getLogger(__name__)


"""
This module provides functions for sending requests to a device.
"""


def capability_request(device):
    """
    """
    # {
    # 	"uuid": "e2bf93b6-9b5d-4944-a863-611b6b6600e7",
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
    #             "group": 0
    #         },
    #         {
    #             "id": 1,
    #             "name": "Read humidity",
    #             "type": 1,
    #             "return_type": 1,
    #             "group": 1
    #         }
    #     ]
    # }
