from abc import ABC, abstractmethod
import networkx as nx

from src.Nodes.buyer import Buyer
from src.Nodes.seller import Seller


class GridInterface(ABC):
    @abstractmethod
    def create(self):
        pass


class simpleGrid(GridInterface):
    def __init__(self, sellers: Seller, buyers: Buyer, conectors: Conectors):
        self.graph = nx.Graph()
        self.graph.add_node_from(sellers + buyers)
