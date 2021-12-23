import random


class Consumer():
    def __init__(self, price, steps):
        demand_amount = random.randin(1, 2)
        self.demand_per_step = [random.randint(0, 1) for i in range(steps)] * demand_amount
        self.bought_per_step = [0] * steps

    def get_demand(self, step):
        return self.demand_per_step(step)
