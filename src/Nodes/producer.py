from collections import Counter

from src.Nodes.node import Node, SettleReturn, BalanceReturn
from src.Nodes.types import NodeTypes


class Producer(Node):
    def clear_up(self, step: int):
        self.sold_per_step[step] = self.supply_per_step[step]

    def __init__(self, supply_per_step, node_type=NodeTypes.PRODUCER):
        self.supply_per_step = supply_per_step
        self.sold_per_step = [0] * len(supply_per_step)
        self.type = node_type

    def get_balance(self, step: int) -> BalanceReturn:
        return BalanceReturn(self.supply_per_step[step], 0, 1, Counter([self.type]))

    def settle(self, step, overflow):
        if overflow >= 0:
            if overflow >= self.supply_per_step[step]:
                return_flow = overflow - self.supply_per_step[step]
                self.sold_per_step[step] = 0
            else:
                return_flow = 0
                self.sold_per_step[step] = self.supply_per_step[step] - overflow
            return SettleReturn(return_flow, self.sold_per_step[step], 0, 1, True)
        else:
            print("settle was given a negativ overflow in in a producer")
