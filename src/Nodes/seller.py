import uuid

from src.Nodes.gridnodes import GridNodeInterface


class Seller(GridNodeInterface):
    def __init__(self):
        self.uuid = uuid.uuid4()

    def get_identifier(self):
        return self.uuid
