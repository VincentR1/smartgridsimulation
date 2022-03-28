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


@dataclass
class DataReturn:
    demand: float
    bought: float
    sold: float
    supply: float
    load: float
    balance_battery: float
    capacity: float
    load: float
    balance_extern: float


class Node(ABC):
    @abstractmethod
    def get_balance(self, step: int) -> BalanceReturn:
        pass

    @abstractmethod
    def settle(self, step: int, overflow: float):
        pass

    # is used to set values in leaves, which haven't been touched during settle
    @abstractmethod
    def clear_up(self, step: int):
        pass

    @abstractmethod
    def extract_data_step(self, step: int) -> DataReturn:
        pass

    # resets a grid after usage
    @abstractmethod
    def clear(self):
        pass
