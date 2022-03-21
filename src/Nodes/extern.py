from collections import Counter

from src.Nodes.node import BalanceReturn, StorageInfo, Node
from src.Nodes.types import NodeTypes


class Extern(Node):
    def clear_up(self, step: int):
        self.activated = False

    def __init__(self, steps):
        self.sold_per_step = [0] * steps
        self.type = NodeTypes.EXTERN
        self.activated = False

    def get_balance(self, step: int) -> BalanceReturn:
        if self.activated:
            return BalanceReturn(balance=self.sold_per_step[step], loss=0, min_eff=1, types=Counter([self.type]),
                                 storage=StorageInfo(0, 0, 0, 0))

        return BalanceReturn(0, 0, 1, Counter([self.type]), StorageInfo(0, 0, 0, 0))

    def settle(self, step, overflow):
        self.activated = True
        self.sold_per_step[step] = -overflow

    def clear(self):
        self.sold_per_step = [0 for i in self.sold_per_step]
