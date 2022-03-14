from random import random

from config import AVRG_CONSUMTION, WINDOW
from src.Nodes.consumer import Consumer
from matplotlib import pyplot as plt


class SimpleConsumer(Consumer):
    def __init__(self, steps, value=10000):
        demand_per_step = [value] * steps
        super().__init__(demand_per_step)


class RandomSingleHouse(Consumer):
    def __init__(self, steps, number_Persons):
        averarage_demand_in_watt_per_person_per_steps = AVRG_CONSUMTION
        demand_per_step = [(random.random() + 1) * averarage_demand_in_watt_per_person_per_steps * WINDOW[i] for i in
                           range(steps)]
        super(demand_per_step)



class DayOnNightOff(Consumer):
    def __init__(self, steps, value=100):
        day_time = [6, 7, 8, 9, 10]
        demand_per_step = [0] * steps
        for i in range(steps):
            if i % 24 in day_time:
                demand_per_step[i] = value
            else:
                demand_per_step[i] = 0
        super().__init__(demand_per_step)


class RandomSwitchingConsumer(Consumer):
    def __init__(self, steps, value=100):
        demand_per_step = [random.randint(0, 1) * value for i in range(steps)]
        super().__init__(demand_per_step)
