import unittest

from src.Nodes.generators.grids.simple_grids import SimpleGrid, SimpleGridWurm
from src.Nodes.node import SettleReturn

transport_eff = 0.8


class TestGrid(unittest.TestCase):
    def test_negative_overflow(self):
        grid = SimpleGrid(steps=1, number_consumer=2, number_producer=1, transportation_eff=transport_eff)
        output: SettleReturn = grid.start(0)
        expected_output = SettleReturn(0, 0, (1 - transport_eff ** 2) * 100, 1, True)
        self.assertAlmostEqual(output.updated_external_loss, expected_output.updated_external_loss)
        self.assertEqual(output.updated_external_balance, expected_output.updated_external_balance)

    def test_positive_overflow(self):
        grid = SimpleGrid(steps=1, number_consumer=1, number_producer=2, transportation_eff=transport_eff)
        output: SettleReturn = grid.start(0)
        expected_output = SettleReturn(0, 0, (1 / transport_eff ** 2 - 1) * 100, 1, True)
        self.assertAlmostEqual(output.updated_external_loss, expected_output.updated_external_loss)
        self.assertEqual(output.updated_external_balance, expected_output.updated_external_balance)

    def test_interconecting_grid(self):
        grid = SimpleGridWurm(steps=1, number_producer=1, number_consumer=1, number_interconecting_grids=13,
                              transport_eff=transport_eff)
        output: SettleReturn = grid.start(0)
        expected_output = SettleReturn(0, 0, (1 - transport_eff ** 13) * 100, 1, True)
        self.assertAlmostEqual(output.updated_external_loss, expected_output.updated_external_loss)
        self.assertEqual(output.updated_external_balance, expected_output.updated_external_balance)


if __name__ == '__main__':
    unittest.main()


def runTest():
    unittest.main()
