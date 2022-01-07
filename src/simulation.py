import numpy as np
import matplotlib.pyplot as plt

from src.Nodes.consumer import Consumer
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
        x = range(self.steps)
        producers = self.grid.get_producers()
        consumers = self.grid.get_consumers()
        fig, axs = plt.subplots(len(consumers), 1)
        fig.suptitle("consumers")
        for i in range(len(consumers)):
            axs[i].plot(x, consumers[i].demand_per_step, 'r', x, consumers[i].bought_per_step)
        fig2, axs2 = plt.subplots(len(producers), 1)
        fig2.suptitle("producers")
        for i in range(len(producers)):
            axs2[i].plot(x, producers[i].supply_per_step, 'r', x, producers[i].sold_per_step)
        plt.show()

    def run(self):
        producers = self.grid.get_producers()
        consumers = self.grid.get_consumers()

        for step in range(self.steps):
            distances = self.grid.get_distances(step)
            production_prices = self.grid.get_prices(step)
            offers = distances * production_prices

            for index_consumer in range(len(consumers)):
                offer = offers[index_consumer]
                bought_from = consumers[index_consumer].give_offer_and_buy(offer, producers, step)
