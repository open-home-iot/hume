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

    def perform_operation(self, device, operation):
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
            print("NOT IMPLEMENTED: Action")

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
