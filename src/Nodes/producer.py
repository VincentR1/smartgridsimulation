import random
import uuid


class Producer:
    def __init__(self, price, steps):
        self.price = price
        supply_amount = random.randint(3, 5)
        self.supply_per_step = [random.randint(0, 1) * supply_amount for i in range(steps)]
        self.sold_per_step = [0] * steps;

    def get_price(self, step):
        return self.price

    def get_amount(self, step):
        return self.price * self.supply_per_step[step]
