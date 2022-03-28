from enum import Enum, auto


class NodeTypes(Enum):
    BATTERY = auto()
    CONSUMER = auto()
    PRODUCER = auto()
    COAL = auto()
    GRID = auto()
    EXTERN = auto()
