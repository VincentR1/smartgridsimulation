import unittest
from collections import Counter

from src.Nodes.extern import Extern
from src.Nodes.generators.grids.simple_grids import SimpleGrid, SimpleGridWurm
from src.Nodes.node import SettleReturn, BalanceReturn, StorageInfo
from src.Nodes.producer import Producer
from src.Nodes.storage import Storage
from src.Nodes.types import NodeTypes

transport_eff = 0.8


class TestGrid(unittest.TestCase):
    def test_negative_overflow(self):
        grid = SimpleGrid(steps=1, number_consumer=2, number_producer=1, transportation_eff=transport_eff)
        output: SettleReturn = grid.start(0)
        expected_output = BalanceReturn(balance=0, loss=(1 - transport_eff ** 2) * 1000, min_eff=transport_eff,
                                        storage=StorageInfo(0, 0, 0, 0),
                                        types=Counter([NodeTypes.CONSUMER, NodeTypes.CONSUMER, NodeTypes.PRODUCER]))
        self.assertAlmostEqual(output.loss, expected_output.loss)
        self.assertEqual(output.balance, expected_output.balance)
        self.assertEqual(output.types, expected_output.types)

    def test_positive_overflow(self):
        grid = SimpleGrid(steps=1, number_consumer=1, number_producer=2, transportation_eff=transport_eff)
        output: BalanceReturn = grid.start(0)
        expected_output = BalanceReturn(balance=0, loss=(1 / transport_eff ** 2 - 1) * 1000, min_eff=transport_eff,
                                        types=Counter([NodeTypes.CONSUMER]), storage=(StorageInfo(0, 0, 0, 0)))
        self.assertAlmostEqual(output.loss, expected_output.loss)
        self.assertEqual(output.balance, expected_output.balance)

    def test_interconecting_grid(self):
        grid = SimpleGridWurm(steps=1, number_producer=1, number_consumer=1, number_interconecting_grids=13,
                              transport_eff=transport_eff)
        output: BalanceReturn = grid.start(0)
        expected_output = BalanceReturn(balance=0, loss=(1 - transport_eff ** 13) * 1000, min_eff=1,
                                        types=Counter([NodeTypes.CONSUMER, NodeTypes.PRODUCER]),
                                        storage=StorageInfo(0, 0, 0, 0))

        self.assertAlmostEqual(output.loss, expected_output.loss)
        self.assertEqual(output.balance, expected_output.balance)

    def test_storage_grid(self):
        grid = SimpleGrid(steps=1, number_producer=1, number_consumer=0, transportation_eff=transport_eff)
        storage = Storage(1, 10000, 0)
        grid.adding_node(storage, transport_eff)
        output: BalanceReturn = grid.start(0)
        self.assertEqual(output.balance, 0)
        self.assertAlmostEqual(output.loss, 1000 * (1 - transport_eff ** 2))
        self.assertEqual(storage.load[0], 6400)

    def test_storage_grid(self):
        grid = SimpleGrid(steps=1, number_producer=1, number_consumer=0, transportation_eff=transport_eff)
        storage = Storage(1, 1000, 980)
        grid.adding_node(storage, transport_eff)
        output: BalanceReturn = grid.start(0)
        self.assertEqual(output.balance, 0)
        self.assertAlmostEqual(output.loss, 200 / transport_eff / transport_eff * (1 - transport_eff ** 2))
        self.assertEqual(storage.load[0], 1000)

    def test_coal(self):
        grid = SimpleGrid(steps=1, number_producer=4, number_consumer=1, transportation_eff=transport_eff)
        coalProducer = Producer([1000], NodeTypes.COAL)
        grid.adding_node(coalProducer, transport_eff=transport_eff)
        output = grid.start(0)
        print(output)
        print(coalProducer.sold_per_step)

    def test_extern_neg(self):
        grid = SimpleGrid(steps=1, number_consumer=1, number_producer=0, transportation_eff=transport_eff)
        extern = Extern(1)
        grid.adding_node(extern, 1)
        output = grid.start(0)
        self.assertEqual(extern.sold_per_step[0], 1000 / transport_eff)

    def test_extern_pos(self):
        grid = SimpleGrid(steps=1, number_consumer=0, number_producer=1, transportation_eff=transport_eff)
        extern = Extern(1)
        grid.adding_node(extern, 1)
        output = grid.start(0)
        self.assertEqual(extern.sold_per_step[0], -1000 * transport_eff)


if __name__ == '__main__':
    unittest.main()


def run_test():
    unittest.main()
