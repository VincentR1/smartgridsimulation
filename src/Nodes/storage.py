from collections import Counter

from src.Nodes.node import Node, BalanceReturn, SettleReturn, StorageInfo
from src.Nodes.types import NodeTypes


class Storage(Node):
    def __init__(self, steps, capacity, load):
        self.capacity = capacity
        self.demand_per_step = [capacity] * steps
        self.load = [0] * steps + 1
        self.balance = 0

    def get_balance(self, step: int) -> BalanceReturn:
        load_in_step = self.load[step]
        capacity_in_step = self.capacity - load_in_step
        return BalanceReturn(balance=self.balance, loss=0, min_eff=1, types=Counter([NodeTypes.BATTERY]), storage=(
            StorageInfo(load=load_in_step, capacity=capacity_in_step, min_dist_consumer=-1, min_dist_producer=-1)))

    def settle(self, step: int, overflow: float):
        if overflow >= 0:
            # load
            if overflow + self.load[step] > self.capacity:
                self.load[step] = self.capacity
                self.balance = self.load[step] - self.capacity
            else:
                self.load[step] += overflow
                self.balance = -overflow
        else:
            # deplete
            if overflow + self.load[step] > 0:
                self.load[step] += overflow
                self.balance = -overflow
            else:
                self.balance = self.load[step]
                self.load[step] = 0

    def clear_up(self, step: int):
        self.load[step + 1] = self.load[step]
        self.balance = 0
        pass
