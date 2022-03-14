from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections import Counter


@dataclass()
class StorageInfo:
    load: float
    capacity: float
    min_dist_consumer: float
    min_dist_producer: float


@dataclass()
class MinEff:
    consumer_to_producer: float
    producer_to_consumer: float


@dataclass
class BalanceReturn:
    balance: float
    loss: float
    min_eff: float
    types: Counter
    storage: StorageInfo


@dataclass
class SettleReturn:
    return_flow: float
    updated_balance: float
    updated_loss: float
    updated_mineff: float
    updated_types: Counter
    updated_storage: StorageInfo
    settled: bool


class Node(ABC):
    @abstractmethod
    def get_balance(self, step: int) -> BalanceReturn:
        pass

    @abstractmethod
    def settle(self, step: int, overflow: float):
        pass

    @abstractmethod
    def clear_up(self, step: int):
        pass
