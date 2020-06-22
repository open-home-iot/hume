import multiprocessing
import random

from traffic_generator.simulator import Device, DeviceConfig, Hint
from traffic_generator.simulator.device import STATIC_DEVICE_ACTIONS


class DeviceSim:
    """
    Simulates what can happen to a device, both device originated and HINT
    origin. Did this to simplify the simulation, keeping all rules in one place.
    Dividing it up into a device origin and HINT origin simulation would mean
    device state needs to be saved in both places, which basically mimics real
    functionality... Now, just need to keep track of acceptable options to
    execute (keeping track of device state) and go for it.
    """

    def __init__(self,
                 device_specs,
                 dc_q: multiprocessing.Queue,
                 hc_q: multiprocessing.Queue,
                 mq: multiprocessing.Queue):
        """
        :param device_specs: devices for the current traffic run
        :param dc_q: DC command queue
        :param hc_q: HC command queue
        :param mq: monitor reporting queue
        """
        self.dc_q = dc_q
        self.hc_q = hc_q
        self.mq = mq

        self.devices: [Device] = self.load_devices(device_specs)
        self.device_config = DeviceConfig()  # None at start, random gen.

        self.hint = Hint()  # Encapsulates HINT actions

    @staticmethod
    def load_devices(device_specs):
        """
        Loads device specs and returns a list of created device objects.

        :param device_specs:
        :return:
        """
        devices = []

        for dev_id, spec in device_specs:
            devices.append(Device(dev_id, spec))

        return devices

    def do_device_originated_action(self, device: Device):
        """
        Tells the simulator to perform a device orignated action for the
        parameter device. The simulator chooses some device originated action to
        perform randomly, but it has to be in accordance with the HOME protocol.

        :param device:
        :return:
        """
        print("doing something device originated")

        possible_actions = device.device_originated_actions + STATIC_DEVICE_ACTIONS
        print("Possible actions:")
        print(possible_actions)

        action_or_event = random.choice(possible_actions)
        print("Chosen action:")
        print(action_or_event)

        self.dc_q.put((device, action_or_event))

    def do_hint_originated_action(self, device: Device):
        """
        Tells the simulator to perform a HINT originated action for the
        parameter device. The simulator chooses some HINT originated action to
        perform randomly, but it has to be in accordance with the HOME protocol.

        :param device:
        :return:
        """
        print("doing something HINT originated")

    def do_something_unexpected(self, device: Device):
        """
        Tells the simulator to perform something unexpected, attempting to
        break the HOME protocol in some way.

        :param device:
        :return:
        """
        print("doing something unexpected")
