from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BalanceReturn:
    balance: float
    loss: float
    min_eff: float
    types: set


@dataclass
class SettleReturn:
    return_flow: float
    updated_external_balance: float
    updated_external_loss: float
    updated_mineff: float
    settled: bool


class Node(ABC):
    ##will return (balance,lost)
    ##balance is the sum of production and demand, connected to this node, if negativ the node has higher demand than production
    ##lost is the amount of energy wich is lost due to transport in total
    ## singel biggest loss
    @abstractmethod
    def get_balance(self, step: int) -> BalanceReturn:
        pass

    @abstractmethod
    def settle(self, step: int, overflow: float) -> SettleReturn:
        pass

    @abstractmethod
    def clear_up(self, step: int):
        pass
