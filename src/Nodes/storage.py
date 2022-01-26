from src.Nodes.node import Node


class Storage(Node):
    def __init__(self, steps, capacity):
        self.demand_per_step = [capacity] * steps
        self.load_per_step = [0] * steps

    def get_balance(self, step: int) -> (float, float, float):
        load_in_step = self.load_per_step[step]
        self.load_per_step[step] = 0
        return load_in_step, 0, 1, {1}

    def settle(self, step: int, overflow: float) -> (float, float, float):
        pass

    @abstractmethod
    def clear_up(self, step: int):
        pass
