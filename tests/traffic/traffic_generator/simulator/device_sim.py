import multiprocessing
import random

from traffic_generator.simulator import Device, Hint


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

        self.devices: [Device] = DeviceSim.load_devices(device_specs)

        self.hint = Hint()  # Encapsulates HINT actions

    def get_device(self, uuid):
        """
        Get a device based on its UUID.

        :param uuid:
        :return:
        """
        for device in self.devices:
            if device.uuid == uuid:
                return device

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

    def origin_device(self, device: Device):
        """
        Tells the simulator to perform a device originated action for the
        parameter device. The simulator chooses some device originated action to
        perform randomly, but it has to be in accordance with the HOME protocol.

        :param device:
        :return:
        """
        possible_operations = device.device_originated_operations
        print("Possible operations:")
        print(possible_operations)

        # Operation tuple identifying device + op
        operation = random.choice(possible_operations)
        print("Chosen operation:")
        print(operation)

        self.mq.put(operation)
        self.dc_q.put(operation)

    def origin_hint(self, device: Device):
        """
        Tells the simulator to perform a HINT originated action for the
        parameter device. The simulator chooses some HINT originated action to
        perform randomly, but it has to be in accordance with the HOME protocol,
        and conforms with the HINT simulator which imposes some constraints on
        what types on configurations may be done.

        :param device:
        :return:
        """
        possible_operations = self.hint.hint_originated_operations
        print("Possible operations: ")
        print(possible_operations)

        operation = random.choice(possible_operations)
        print("Chosen operation:")
        print(operation)

        # Make HINT simulator perform the necessary things on the HINT end and
        # return what needs to be sent onward to HUME.
        operation_info = self.hint.perform_operation(device, operation)

        self.hc_q.put((device, operation_info))

    def origin_chaos(self, device: Device):
        """
        Tells the simulator to perform something unexpected, attempting to
        break the HOME protocol in some way.

        :param device:
        :return:
        """
        pass
