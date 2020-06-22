import os
import json

from traffic_generator.simulator import Device

device_spec_path = \
        f"{os.path.dirname(os.path.abspath(__file__))}/devices"


def load_device_specs():
    """
    Loads device specifications listed under ./specs/devices.

    :return: list of loaded devices
    """
    devices = []

    for spec in os.listdir(device_spec_path):
        with open(f"{device_spec_path}/{spec}", 'r') as fp:
            dev_str, _file_type = spec.split('.')
            _dev_prefix, dev_id = dev_str.split('_')
            devices.append((dev_id, json.load(fp)))

    return devices


def get_device_spec(device: Device):
    """
    Gets the pointed out device spec.

    :param device:
    :return: device spec
    """
    with open(f"{device_spec_path}/dev_{device.htt_id}.json", 'r') as fp:
        return json.load(fp)


class HTTSettings:

    def __init__(self, htt_settings):
        """
        :param htt_settings: dict of HTT settings
        """
        self.chaos_element = htt_settings.get("chaos_element", False)
        self.actions_per_minute = htt_settings.get("actions_per_minute", 1.0)


def load_htt_specs():
    """
    Loads HTT specifications listed under ./specs/htt.

    :return: HTT settings object
    """
    htt_spec_path = f"{os.path.dirname(os.path.abspath(__file__))}/htt"

    with open(f"{htt_spec_path}/htt.json", 'r') as fp:
        htt_settings = json.load(fp)

        return HTTSettings(htt_settings)
