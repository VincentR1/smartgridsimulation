import numpy as np
import matplotlib.pyplot as plt

from src.grid import Grid


class Simulation:
    def __init__(self, grid: Grid, steps: int):
        self.grid = grid
        if grid.steps != steps:
            raise ValueError
        self.steps = steps

        self.losses_on_network = [0] * steps
        self.overproduction = [0] * steps
        self.fullfild_demand_rel = [0] * steps
        self.consumers = self.grid.consumers
        self.producers = self.grid.producers

        self.demand_unfullfild_consumer = [[0] * steps] * len(self.consumers)

    def plot(self):
        fig, axs = plt.subplots(len(self.consumers))
        fig.suptitle('demands over time')
        for i in range(len(self.consumers)):
            print(self.consumers[i].demand_per_step)
            axs[i].plot(range(self.steps), self.consumers[i].demand_per_step)

        plt.imshow(img.reshape((28, 28)))
        plt.show()

    def run(self):

        for step in range(self.steps):
            distances = self.grid.get_distances(step)
            production_prices = self.grid.get_prices(step)
            production_amounts = self.grid.get_amounts(step)
            production_amounts_left_in_cash = production_amounts * production_prices
            consumer_demands = self.grid.get_demands(step)
            offers = distances * production_prices

            for i in range(len(consumer_demands)):
                offer = offers[i]  # [(price1),( price2)]
                demand = consumer_demands[i]

                min_offer_set = set(offer)
                for min_offer in min_offer_set:
                    min_indexes = np.where(offer == min_offer)[0]
                    price_for_demand = min_offer * demand;

                    for min_index in min_indexes:
                        if production_amounts_left_in_cash[min_index] - price_for_demand >= 0:
                            production_amounts_left_in_cash[min_index] = production_amounts_left_in_cash[
                                                                             min_index] - price_for_demand
                            consumer_demands[i] = 0
                            break
                        else:
                            consumer_demands[i] = consumer_demands[i] - production_amounts_left_in_cash[min_index]
                            production_amounts_left_in_cash[min_index] = 0
                    if consumer_demands[i] >= 0:
                        break

                self.demand_unfullfild_consumer[i][step] = consumer_demands[i]
