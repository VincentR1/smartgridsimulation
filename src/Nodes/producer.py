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

    def get_sold_per_step(self, step):
        return self.sold_per_step[step]

    def buy(self, amount_cash, step):
        supply_cash = (self.get_amount(step) - self.get_sold_per_step(step)) * self.get_price(step)
        if supply_cash - amount_cash >= 0:
            self.sold_per_step[step] = self.sold_per_step[step] + amount_cash / self.get_price(step)
            return amount_cash
        else:
            self.sold_per_step[step] = self.supply_per_step[step]
            return supply_cash
