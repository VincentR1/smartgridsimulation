import random
import numpy as np


class Consumer():
    def __init__(self, steps):
        demand_amount = random.randint(1, 1)
        self.demand_per_step = [random.randint(0, 1) * demand_amount for i in range(steps)]
        self.bought_per_step = [0] * steps

    def get_demand(self, step):
        return self.demand_per_step[step]

    def give_offer_and_buy(self, offers, producers, step):
        bought_from = []
        demand = self.demand_per_step[step]
        min_offers_set = set(offers)
        print((min_offers_set))
        for min_offer in min_offers_set:
            min_indexs = np.where(offers == min_offer)[0]
            print(min_indexs)
            demand_cash = min_offer * demand
            for min_index in min_indexs:
                demand = demand - producers[min_index].buy(demand_cash, step) / min_offer
                bought_from.append(min_index)
                if demand <= 0:
                    break
            if demand <= 0:
                break
        self.bought_per_step[step] = self.demand_per_step[step] - demand
        return bought_from
