import math
import random

import matplotlib.pyplot as plt
import numpy
import numpy as np

from src.Nodes.consumer import Consumer


class SimpleConsumer(Consumer):
    def __init__(self, steps, value=1000):
        demand_per_step = [value] * steps
        super().__init__(demand_per_step)


class DayOnNightOff(Consumer):
    def __init__(self, steps, value=20000):
        day_time = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        demand_per_step = [0] * steps
        for i in range(steps):
            if i % 24 in day_time:
                demand_per_step[i] = value
            else:
                demand_per_step[i] = 0
        super().__init__(demand_per_step)


class RandomSwitchingConsumer(Consumer):
    def __init__(self, steps, value=2000):
        demand_per_step = [random.randint(0, 1) * value + random.randint(0, 1) * value + random.randint(0, 1) * value
                           for i in range(steps)]
        super().__init__(demand_per_step)


class RandomConsumer(Consumer):
    def __init__(self, steps, value=3600):
        sigma = 3
        daytime_window = [0.2, 0.2, 0.3, 0.5,
                          0.7, 1.3, 1.4, 1.4,
                          1, 0.7, .9, 1.2,
                          1.3, 1, 0.8, 1, 2,
                          3, 2, 1, 0.8, 0.4,
                          0.3, 0.2]

        demand_per_step = [random.random() * 2 * value * daytime_window[i % 24]
                           for i in range(steps)]
        super().__init__(demand_per_step)


class Fabric(Consumer):
    def __init__(self, steps, value=50000, schwankung=.2):
        demand = [((random.random() * schwankung) + (1 - schwankung / 2) * value) for i in range(steps)]
        super().__init__(demand)


if __name__ == "__main__":
    steps = 7 * 24
    h = RandomConsumer(steps=steps)
    print(np.mean(h.demand_per_step))
    plt.plot(h.demand_per_step)

    plt.show()
