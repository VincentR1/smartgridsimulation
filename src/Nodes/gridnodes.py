from abc import ABC, abstractmethod

class GridNodeInterface(ABC):
    @abstractmethod
    def get_identifier(self):
        pass
