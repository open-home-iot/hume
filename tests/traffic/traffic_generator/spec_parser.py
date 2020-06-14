import os
import json


def load_device_specs():
    """
    Loads device specifications listed under ./specs/devices.

    :return: list of loaded devices
    """
    devices = []

    device_spec_path = \
        f"{os.path.dirname(os.path.abspath(__file__))}/specs/devices"

    for spec in os.listdir(device_spec_path):
        with open(f"{device_spec_path}/{spec}", 'r') as fp:
            devices.append(json.load(fp))

    return devices


class HTTSettings:

    def __init__(self, htt_settings):
        """
        :param htt_settings: dict of HTT settings
        """
        self.chaos_element = htt_settings.get("chaos_element", False)


def load_htt_specs():
    """
    Loads HTT specifications listed under ./specs/htt.

    :return: HTT settings object
    """
    htt_spec_path = f"{os.path.dirname(os.path.abspath(__file__))}/specs/htt"

    with open(f"{htt_spec_path}/htt.json", 'r') as fp:
        htt_settings = json.load(fp)

        return HTTSettings(htt_settings)
