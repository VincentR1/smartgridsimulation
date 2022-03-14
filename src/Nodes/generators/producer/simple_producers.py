from random import random
from src.Nodes.producer import Producer


class SimpleProducer(Producer):
    def __init__(self, steps, value=10000):
        super().__init__(supply_per_step=[value] * steps)


class RandomSwitchingProducer(Producer):
    def __init__(self, steps, value=10000):
        supply_per_step = [random.randint(0, 1) * value for i in range(steps)]
        super().__init__(self, supply_per_step)
