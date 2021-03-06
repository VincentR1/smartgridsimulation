from collections import Counter

from src.Nodes.node import Node, SettleReturn, BalanceReturn, StorageInfo, DataReturn
from src.Nodes.types import NodeTypes


class Consumer(Node):
    def extract_data_step(self, step: int) -> DataReturn:

        ret = DataReturn(demand=self.demand_per_step[step], bought=self.bought_per_step[step], load=0,
                         balance_extern=0, sold=0,
                         balance_battery=0, supply=0, capacity=0)
        return ret

    def __init__(self, demand_per_step, node_type=NodeTypes.CONSUMER):
        self.demand_per_step = demand_per_step
        self.bought_per_step = [0] * len(demand_per_step)
        self.type = node_type
        self.activated = False

    def clear_up(self, step: int):
        if not self.activated:
            self.bought_per_step[step] = self.demand_per_step[step]
        self.activated = False

    def get_balance(self, step: int) -> BalanceReturn:
        if self.activated:
            return BalanceReturn(-self.bought_per_step[step], 0, 1, Counter([self.type]), StorageInfo(0, 0, 0, 0))
        else:
            return BalanceReturn(-self.demand_per_step[step], 0, 1, Counter([self.type]), StorageInfo(0, 0, 0, 0))

    def settle(self, step, overflow):
        if self.activated:
            print('Itsme again')
        self.activated = True
        if overflow <= 0:
            if -overflow >= self.demand_per_step[step]:
                self.bought_per_step[step] = 0
            else:
                self.bought_per_step[step] = self.demand_per_step[step] + overflow

        else:
            print("settle was given a positiv overflow in in a consumer")

    def clear(self):
        self.bought_per_step = [0 for b in self.bought_per_step]
