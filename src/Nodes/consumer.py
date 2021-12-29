import random


class Consumer():
    def __init__(self, steps):
        demand_amount = random.randint(1, 2)
        self.demand_per_step = [random.randint(0, 1) * demand_amount for i in range(steps)]
        self.bought_per_step = [0] * steps

    def get_demand(self, step):
        return self.demand_per_step[step]
