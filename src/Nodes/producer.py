import random
import uuid

from src.Nodes.node import Node


class Producer(Node):
    def clear_up(self, step: int):
        self.sold_per_step[step] = self.supply_per_step[step]

    def __init__(self, supply_per_step):
        self.supply_per_step = supply_per_step
        self.sold_per_step = [0] * len(supply_per_step)

    def get_balance(self, step: int) -> (float, float):
        return self.supply_per_step[step], 0, 1

    def settle(self, step, overflow):
        if overflow >= 0:
            if overflow >= self.supply_per_step[step]:
                return_flow = overflow - self.supply_per_step[step]
                self.sold_per_step[step] = 0
            else:
                return_flow = 0
                self.sold_per_step[step] = self.supply_per_step[step] - overflow
            return return_flow, self.sold_per_step[step], 0, 1, True
        else:
            print("settle was given a negativ overflow in in a producer")
