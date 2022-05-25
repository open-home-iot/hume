from enum import Enum


class HintMessage(Enum):
    DISCOVER_DEVICES = 0
    ATTACH = 1

    ACTION_STATEFUL = 2
    ACTION_STATES = 5

    UNPAIR = 3
    DETACH = 4
