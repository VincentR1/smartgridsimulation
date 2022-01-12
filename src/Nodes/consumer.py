import random
import numpy as np

from src.Nodes.node import Node


class Consumer(Node):
    def __init__(self, steps):
        demand_amount = random.randint(1, 1)
        self.demand_per_step = [random.randint(0, 1) * demand_amount for i in range(steps)]
        self.bought_per_step = [0] * steps

    def get_balance(self, step: int) -> (float, float):
        return -self.demand_per_step[step], 0

    def settle(self, step, overflow):
        if overflow <= 0:
            self.bought_per_step[step] = self.demand_per_step[step] + overflow
        else:
            print("settle was given a positiv overflow in in a consumer")
