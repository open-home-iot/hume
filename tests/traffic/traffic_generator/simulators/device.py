def indent(level):
    i = 0
    ind = ""

    while i < level:
        ind = f"{ind}  "
        i += 1

    return ind


class Device:

    def __init__(self, device_spec: dict):
        """
        :param device_spec: spec for the device to be created
        """
        self.name = device_spec["name"]
        self.uuid = device_spec.get("uuid")
        self.cls = device_spec["class"]
        self.spec = device_spec["spec"]
        self.devices = self.load_sub_devices(device_spec.get("devices"))
        self.actions = self.load_device_actions(device_spec.get("actions"))
        self.events = self.load_device_events(device_spec.get("events"))

    @staticmethod
    def load_sub_devices(sub_device_specs):
        """
        Loads sub devices and returns a list of created devices.

        :param sub_device_specs:
        :return:
        """
        if sub_device_specs is None:
            return []

        sub_devices = []

        for spec in sub_device_specs:
            sub_devices.append(Device(spec))

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

        if self.actions:
            for action in self.actions:
                actions += f"{action.__str__()}"

        if self.events:
            for event in self.events:
                events += f"{event.__str__()}"

        return f"{indent(level)}{self.name}:\n" \
               f"{indent(level + 1)}actions: {actions}\n" \
               f"{indent(level + 1)}events: {events}\n" \
               f"{indent(level + 1)}sub-devices: \n{sub_devices}"


class DeviceAction:

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


class DeviceEvent:

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
