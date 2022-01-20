import random
import uuid


class Producer:
    def __init__(self, supply_per_step):
        self.supply_per_step = supply_per_step
        self.sold_per_step = [0] * len(supply_per_step)

    def get_balance(self, step: int) -> (float, float):
        return self.supply_per_step[step], 0, 1

    def settle(self, step, overflow):
        if overflow >= 0:
            self.sold_per_step[step] = self.supply_per_step[step] - overflow
        else:
            print("settle was given a positiv overflow in in a consumer")
