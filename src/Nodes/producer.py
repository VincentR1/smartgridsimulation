from collections import Counter

from src.Nodes.node import Node, SettleReturn, BalanceReturn, StorageInfo, DataReturn
from src.Nodes.types import NodeTypes


class Producer(Node):
    def extract_data_step(self, step: int) -> DataReturn:
        return DataReturn(demand=0, bought=0, sold=self.sold_per_step[step], supply=self.supply_per_step[step],
                          balance_extern=0,
                          load=0, capacity=0, balance_battery=0)

    def clear_up(self, step: int):
        if not self.activated:
            self.sold_per_step[step] = self.supply_per_step[step]
        self.activated = False

    def __init__(self, supply_per_step, node_type=NodeTypes.PRODUCER):
        self.supply_per_step = supply_per_step
        self.sold_per_step = [0] * len(supply_per_step)
        self.type = node_type
        self.activated = False

    def get_balance(self, step: int) -> BalanceReturn:
        if self.activated:
            return BalanceReturn(self.sold_per_step[step], 0, 1, Counter([self.type]), StorageInfo(0, 0, 0, 0))

        return BalanceReturn(self.supply_per_step[step], 0, 1, Counter([self.type]), StorageInfo(0, 0, 0, 0))

    def settle(self, step, overflow):
        self.activated = True
        if overflow >= 0:
            if overflow >= self.supply_per_step[step]:
                self.sold_per_step[step] = 0
            else:
                self.sold_per_step[step] = self.supply_per_step[step] - overflow
        else:
            print("settle was given a negativ overflow in in a producer")

    def clear(self):
        self.sold_per_step = [0 for i in self.sold_per_step]
