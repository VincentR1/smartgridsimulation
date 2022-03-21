from collections import Counter

from src.Nodes.node import Node, BalanceReturn, SettleReturn, StorageInfo
from src.Nodes.types import NodeTypes


class Storage(Node):
    def __init__(self, steps, capacity, load):
        self.capacity = capacity
        if load > capacity:
            raise Exception('load must smaler capacity')
        self.load = [load] * (steps + 1)
        self.sold_per_step = [0] * steps

    def get_balance(self, step: int) -> BalanceReturn:
        load_in_step = self.load[step]
        capacity_in_step = self.capacity - load_in_step
        return BalanceReturn(balance=self.sold_per_step[step], loss=0, min_eff=1, types=Counter([NodeTypes.BATTERY]),
                             storage=(
                                 StorageInfo(load=load_in_step, capacity=capacity_in_step, min_dist_consumer=-1,
                                             min_dist_producer=-1)))

    def settle(self, step: int, overflow: float):
        print('battery called in step:' + str(step) + 'with: ' + str(overflow))

        if overflow >= 0:
            if overflow + self.load[step] > self.capacity:
                self.sold_per_step[step] = self.load[step] - self.capacity
                self.load[step] = self.capacity
            else:
                self.load[step] += overflow
                self.sold_per_step[step] = -overflow
        else:
            # deplete
            if overflow + self.load[step] > 0:
                self.load[step] += overflow
                self.sold_per_step[step] = -overflow
            else:
                self.sold_per_step[step] = self.load[step]
                self.load[step] = 0

    def clear_up(self, step: int):
        self.load[step + 1] = self.load[step]

        pass
