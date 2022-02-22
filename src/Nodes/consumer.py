import random
import numpy as np

from src.Nodes.node import Node, SettleReturn, BalanceReturn


class Consumer(Node):
    def __init__(self, demand_per_step):
        self.demand_per_step = demand_per_step
        self.bought_per_step = [0] * len(demand_per_step)

    def clear_up(self, step: int):
        self.bought_per_step[step] = self.demand_per_step[step]

    def get_balance(self, step: int) -> (float, float, float):
        return BalanceReturn(-self.demand_per_step[step], 0, 1, {})

    def settle(self, step, overflow):
        if overflow <= 0:
            if -overflow >= self.demand_per_step[step]:
                return_flow = overflow + self.demand_per_step[step]
                self.bought_per_step[step] = 0
            else:
                return_flow = 0
                self.bought_per_step[step] = self.demand_per_step[step] + overflow
            return SettleReturn(return_flow, -self.bought_per_step[step], 0, 1, 1)
        else:
            print("settle was given a positiv overflow in in a consumer")
