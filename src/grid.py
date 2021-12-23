from abc import ABC, abstractmethod
import networkx as nx

from src.Nodes.consumer import Consumer
from src.Nodes.producer import Producer


class Grid:
    def __init__(self):
        steps = 100
        self.producers = [Producer(steps), Producer(steps)]
        self.consumers = [Consumer(steps), Consumer(steps), Consumer(steps), Consumer(steps), Consumer(steps)]
        self.mat = [[1] * 5, [1] * 5]

    def do_step(self, step):

