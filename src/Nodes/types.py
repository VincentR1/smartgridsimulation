from enum import Enum, auto


class NodeTypes(Enum):
    BATTERY = auto()
    CONSUMER = auto()
    PRODUCER = auto()
    GRID = auto()
