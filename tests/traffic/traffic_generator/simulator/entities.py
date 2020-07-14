import random


def indent(level):
    i = 0
    ind = ""

    while i < level:
        ind = f"{ind}  "
        i += 1

    return ind


class Device:

    ATTACH = "attach"
    EVENT = "event"

    STATIC_DEVICE_OPERATIONS = [
        ATTACH
    ]

    def __init__(self, htt_id, device_spec: dict, parent=None):
        """
        :param htt_id: HTT specific ID for this device
        :param device_spec: spec for the device to be created
        """
        # HTT specific information
        self.htt_id = htt_id

        # Device or None
        self.parent = parent

        # Device general information
        self.name = device_spec["name"]

        # Top device
        self.uuid = device_spec.get("uuid")

        # Sub-device
        self.id = device_spec.get("id")

        self.cls = device_spec["class"]
        self.spec = device_spec["spec"]

        self.devices = self.load_sub_devices(device_spec.get("devices"))
        self._actions = self.load_device_actions(device_spec.get("actions"))
        self._events = self.load_device_events(device_spec.get("events"))

        # Device runtime information
        self._attached = False

    @property
    def attached(self):
        """
        Returns if the device is attached or not.

        :return:
        """
        if not self.parent:
            return self._attached

        return self.parent.attached

    @attached.setter
    def attached(self, attached):
        """
        Sets if the device is attached.

        :param attached:
        :return:
        """
        if not self.parent:
            self._attached = attached
        else:
            self.parent._attached = attached

    @property
    def device_originated_operations(self):
        """
        Retrieve a list of possible actions for this device to take, both on top
        and sub-device levels. Sub devices can be noticed by checking the data
        type of the id of the tuple, sub devices have integer IDs top devices
        have string UUIDs.

        :return:
        """
        # Tuple notation since there is a need to differentiate between events
        # belonging to a sub device versus a top device.
        device_ops = [(self, Device.ATTACH)]

        for event in self._events:
            device_ops.append((self, event))

        for dev in self.devices:
            for event in dev._events:
                device_ops.append((dev, event))

        return device_ops

    def load_sub_devices(self, sub_device_specs):
        """
        Loads sub devices and returns a list of created devices.

        :param sub_device_specs:
        :return:
        """
        if sub_device_specs is None:
            return []

        sub_devices = []

        for spec in sub_device_specs:
            sub_devices.append(Device("sub", spec, parent=self))

        return sub_devices

    @staticmethod
    def load_device_actions(action_specs):
        """
        Loads action specs and returns a list of created actions.

        :param action_specs:
        :return:
        """
        if action_specs is None:
            return []

        actions = []

        for spec in action_specs:
            actions.append(DeviceAction(spec))

        return actions

    @staticmethod
    def load_device_events(event_specs):
        """
        Load event specs and returns a list of created events.

        :param event_specs:
        :return:
        """
        if event_specs is None:
            return []

        events = []

        for spec in event_specs:
            events.append(DeviceEvent(spec))

        return events

    def __str__(self, level=0):
        sub_devices = ""
        actions = ""
        events = ""

        if self.devices:
            for device in self.devices:
                sub_devices += f"{device.__str__(level=level + 2)}"

        if self._actions:
            for action in self._actions:
                actions += f"{action.__str__()}"

        if self._events:
            for event in self._events:
                events += f"{event.__str__()}"

        return f"{indent(level)}{self.name}:\n" \
               f"{indent(level + 1)}actions: {actions}\n" \
               f"{indent(level + 1)}events: {events}\n" \
               f"{indent(level + 1)}sub-devices: \n{sub_devices}"

    def __repr__(self):
        return f"<HTT Device> {self.htt_id}"


class Hint:

    CONFIG_TIMER = "config_timer"
    CONFIG_SCHEDULE = "config_schedule"
    CONFIG_TRIGGER = "config_trigger"

    CONFIRM_ATTACH = "confirm_attach"
    DETACH = "detach"

    ACTION = "action"

    STATIC_HINT_OPERATIONS = [
        CONFIG_TIMER, CONFIG_SCHEDULE, CONFIG_TRIGGER, CONFIRM_ATTACH, DETACH,
        ACTION
    ]

    def __init__(self):
        """"""
        self.device_config = dict()

    @property
    def hint_originated_operations(self):
        """
        Returns a list of HINT originated actions possible.

        :return:
        """
        return Hint.STATIC_HINT_OPERATIONS

    @staticmethod
    def filter_ops_based_on_device_cap(operations, device):
        """
        Filters operations that the parameter device cannot perform due to
        missing capabilities.

        :param operations:
        :param device:
        :return:
        """
        filter_list = []

        # device.attached is a property that checks the parent if sub device.
        if device.attached:
            filter_list.append(Hint.CONFIRM_ATTACH)
        else:
            # can't detach if not attached
            filter_list.append(Hint.DETACH)

        # Implicit booleanness states that an empty list = false
        if not device._actions:
            filter_list.append(Hint.ACTION)
            filter_list.append(Hint.CONFIG_TIMER)
            filter_list.append(Hint.CONFIG_SCHEDULE)

        print(filter_list)
        filtered_ops = [op for op in operations if op not in filter_list]
        print(f"Filtered list of operations: {filtered_ops}")

        return filtered_ops

    def perform_operation(self, device: Device, operation):
        """
        Performs the action on the HINT side and returns information to send to
        HUME. In HTT, that means information to forward to the HC supervisor to
        make a direct call.

        :param device:
        :param operation:
        :return:
        """
        if operation == Hint.CONFIRM_ATTACH:
            device.attached = True

            return operation

        elif operation == Hint.ACTION:
            action = random.choice(device._actions)

            return action

        elif operation == Hint.DETACH:
            print("NOT IMPLEMENTED: Detach")

        elif operation == Hint.CONFIG_TIMER:
            print("NOT IMPLEMENTED: Config timer")

        elif operation == Hint.CONFIG_SCHEDULE:
            print("NOT IMPLEMENTED: Config schedule")

        elif operation == Hint.CONFIG_TRIGGER:
            print("NOT IMPLEMENTED: Config trigger")

        else:
            print("Hint got unrecognized operation")

        # TODO catch all for operation info return!
        return operation


class DeviceAction:

    # Actions are of HINT origin.
    operation_tag = Hint.ACTION

    def __init__(self, action_spec: dict):
        """
        :param action_spec: spec for the action to be created
        """
        self.name = action_spec["name"]
        self.id = action_spec["id"]
        self.type = action_spec["type"]

        if self.type == "STATEFUL":
            self.states = action_spec["states"]
        elif self.type == "READ":
            self.return_type = action_spec["return_type"]

    def __str__(self):
        if self.type == "STATEFUL":
            add_type_str = f"{self.states}"
        elif self.type == "READ":
            add_type_str = f"{self.return_type}"

        return f"[id: {self.id} type: {self.type} -> {add_type_str}] | "

    def __repr__(self):
        if self.type == "STATEFUL":
            add_type_str = f"{self.states}"
        elif self.type == "READ":
            add_type_str = f"{self.return_type}"

        return f"[id: {self.id} type: {self.type} -> {add_type_str}]"


class DeviceEvent:

    operation_tag = Device.EVENT

    def __init__(self, event_spec: dict):
        """
        :param event_spec: spec for the event to be created
        """
        self.description = event_spec["description"]
        self.type = event_spec["type"]
        self.id = event_spec["id"]
        self.data_type = event_spec.get("data_type")

    def __str__(self):
        data_type_str = f" -> {self.data_type}" if self.data_type is not None else ""

        return f"[id: {self.id} type: {self.type}{data_type_str}] | "

    def __repr__(self):
        data_type_str = f" -> {self.data_type}" if self.data_type is not None else ""

        return f"[id: {self.id} type: {self.type}{data_type_str}]"
