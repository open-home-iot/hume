from enum import Enum


class HintMessage(Enum):
    DISCOVER_DEVICES = 0
    ATTACH = 1
    ACTION_STATEFUL = 2
    UNPAIR = 3
    DETACH = 4
