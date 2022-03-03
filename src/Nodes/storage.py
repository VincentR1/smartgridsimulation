from collections import Counter

from src.Nodes.node import Node, BalanceReturn
from src.Nodes.types import NodeTypes


class Storage(Node):
    def __init__(self, steps, capacity):
        self.demand_per_step = [capacity] * steps
        self.load_per_step = [0] * steps

    def get_balance(self, step: int) -> (float, float, float):
        load_in_step = self.load_per_step[step]
        self.load_per_step[step] = 0
        return BalanceReturn(load_in_step, 0, 1, Counter([NodeTypes.BATTERY]))

    def settle(self, step: int, overflow: float) -> (float, float, float):
        pass

    def clear_up(self, step: int):
        pass
