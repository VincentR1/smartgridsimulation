from abc import ABC, abstractmethod


class Node(ABC):
    ##will return (balance,lost)
    ##balance is the sum of production and demand, connected to this node, if negativ the node has higher demand than production
    ##lost is the amount of energy wich is lost due to transport in total
    ## singel biggest loss
    @abstractmethod
    def get_balance(self, step: int) -> (float, float, float):
        pass

    @abstractmethod
    def settle(self, step: int, overflow: float) -> (float, float, float):
        pass
