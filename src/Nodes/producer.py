import random
import uuid


class Producer:
    def __init__(self, price, steps):
        self.price = price
        supply_amount = random.randint(3, 5)
        self.supply_per_step = [random.randint(0, 1) * supply_amount for i in range(steps)]
        self.sold_per_step = [0] * steps

    def get_balance(self, step: int) -> (float, float):
        return self.supply_per_step[step], 0

    def settle(self, step, overflow):
        if overflow >= 0:
            self.sold_per_step[step] = self.supply_per_step[step] - overflow
        else:
            print("settle was given a positiv overflow in in a consumer")
