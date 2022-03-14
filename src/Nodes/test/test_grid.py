import unittest
from collections import Counter

from src.Nodes.generators.grids.simple_grids import SimpleGrid, SimpleGridWurm
from src.Nodes.node import SettleReturn, BalanceReturn, StorageInfo
from src.Nodes.storage import Storage
from src.Nodes.types import NodeTypes

transport_eff = 0.8


class TestGrid(unittest.TestCase):
    def test_negative_overflow(self):
        grid = SimpleGrid(steps=1, number_consumer=2, number_producer=1, transportation_eff=transport_eff)
        output: SettleReturn = grid.start(0)
        expected_output = BalanceReturn(balance=0, loss=(1 - transport_eff ** 2) * 100, min_eff=transport_eff,
                                        storage=StorageInfo(0, 0, 0, 0),
                                        types=Counter([NodeTypes.CONSUMER, NodeTypes.CONSUMER, NodeTypes.PRODUCER]))
        self.assertAlmostEqual(output.loss, expected_output.loss)
        self.assertEqual(output.balance, expected_output.balance)
        self.assertEqual(output.updated_types, expected_output.updated_types)

    def test_positive_overflow(self):
        grid = SimpleGrid(steps=1, number_consumer=1, number_producer=2, transportation_eff=transport_eff)
        output: SettleReturn = grid.start(0)
        expected_output = SettleReturn(0, 0, (1 / transport_eff ** 2 - 1) * 100, 1, Counter([NodeTypes.CONSUMER]), True)
        self.assertAlmostEqual(output.updated_loss, expected_output.updated_loss)
        self.assertEqual(output.updated_balance, expected_output.updated_balance)

    def test_interconecting_grid(self):
        grid = SimpleGridWurm(steps=1, number_producer=1, number_consumer=1, number_interconecting_grids=13,
                              transport_eff=transport_eff)
        output: SettleReturn = grid.start(0)
        expected_output = SettleReturn(0, 0, (1 - transport_eff ** 13) * 100, 1,
                                       Counter([NodeTypes.CONSUMER, NodeTypes.PRODUCER]), True)

        self.assertAlmostEqual(output.updated_loss, expected_output.updated_loss)
        self.assertEqual(output.updated_balance, expected_output.updated_balance)

    def test_storage_grid(self):
        grid = SimpleGrid(steps=1, number_producer=1, number_consumer=0, transportation_eff=transport_eff)
        storage = Storage(1, 1)
        grid.adding_node(storage, transport_eff)
        grid.get_balance(0)
        balance = grid.get_balance(0)


if __name__ == '__main__':
    unittest.main()


def run_test():
    unittest.main()
