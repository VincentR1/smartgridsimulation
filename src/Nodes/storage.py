from collections import Counter

from src.Nodes.node import Node, BalanceReturn, SettleReturn, StorageInfo, DataReturn
from src.Nodes.types import NodeTypes


class Storage(Node):
    def extract_data_step(self, step: int) -> DataReturn:
        return DataReturn(demand=0, supply=0, sold=0, bought=0, load=self.load_per_step[step],
                          balance_battery=self.sold_per_step[step],
                          capacity=self.capacity, balance_extern=0)

    def __init__(self, steps, capacity, load):
        self.starting_load = load
        self.capacity = capacity
        if load > capacity:
            raise Exception('load must smaler capacity')
        self.load_per_step = [load] * (steps + 1)
        self.sold_per_step = [0] * steps

    def get_balance(self, step: int) -> BalanceReturn:
        load_in_step = self.load_per_step[step]
        capacity_in_step = self.capacity - load_in_step
        return BalanceReturn(balance=self.sold_per_step[step], loss=0, min_eff=1, types=Counter([NodeTypes.BATTERY]),
                             storage=(
                                 StorageInfo(load=load_in_step, capacity=capacity_in_step, min_dist_consumer=-1,
                                             min_dist_producer=-1)))

    def settle(self, step: int, overflow: float):

        if overflow >= 0:
            if overflow + self.load_per_step[step] > self.capacity:

                self.sold_per_step[step] = self.load_per_step[step] - self.capacity
                self.load_per_step[step] = self.capacity
            else:
                self.load_per_step[step] += overflow
                self.sold_per_step[step] = -overflow
        else:
            # deplete
            if overflow + self.load_per_step[step] > 0:
                self.load_per_step[step] += overflow
                self.sold_per_step[step] = -overflow
            else:
                self.sold_per_step[step] = self.load_per_step[step]
                self.load_per_step[step] = 0

    def clear_up(self, step: int):
        self.load_per_step[step + 1] = self.load_per_step[step]

        pass

    def clear(self):
        self.load_per_step = [self.starting_load for i in self.load_per_step]
