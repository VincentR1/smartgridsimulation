import numpy as np
from src.Nodes.consumer import Consumer
from src.Nodes.producer import Producer


class Grid:
    def __init__(self, steps: int):
        self.steps = steps
        self.producers = [Producer(1, steps), Producer(1, steps)]
        self.consumers = [Consumer(steps), Consumer(steps), Consumer(steps), Consumer(steps), Consumer(steps)]
        self.mat = [[1] * 2] * 5

    def get_amounts(self, step):
        return np.array([producer.get_amount(step) for producer in self.producers])

    def get_prices(self, step):
        return np.array([producer.get_price(step) for producer in self.producers])

    def get_demands(self, step):
        return np.array([consumer.get_demand(step) for consumer in self.consumers])

    def get_distances(self, step):
        # matrix
        #   p1|p2
        # c1 1  2
        # c2 0  1
        # c3 3  3
        return np.array(self.mat)

    def get_steps(self):
        return self.steps
