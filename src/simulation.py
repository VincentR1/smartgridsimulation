import matplotlib.pyplot as plt

from src.Nodes.generators.grids.city import get_city, get_green_city
from src.Nodes.generators.producer.solar_producer import get_sun_power
from src.Nodes.generators.producer.wind_producer import get_random_wind_velocities
from src.Nodes.grid import Grid, AllData


class Simulator:
    def __init__(self, grid: Grid, steps: int, name: str, extern: False):
        self.grid = grid
        self.steps = steps
        self.data = AllData([0] * steps, [0] * steps, [0] * steps, [0] * steps, [0] * steps, [0] * steps,
                            [0] * steps, [0] * steps)
        self.extern = extern
        self.name = name

    def run(self):
        self.grid.run_simulation()
        self.data = self.grid.extract_data()

    def plot(self):
        x = range(self.steps)
        fig = plt.figure()
        fig.suptitle('name')

        ax_demand = fig.add_subplot(211)
        ax_demand.plot(x, self.data.demand, x, self.data.sold)
        ax_demand.set_ylabel('Wh')
        ax_demand.set_title('demand consumer')

        ax_demand.plot()

        plt.show()

    def clear(self):
        self.grid.clear()


if __name__ == "__main__":
    steps = 24 * 7
    grid = get_green_city(steps=steps, number=5, wind=get_random_wind_velocities(steps),
                          sun=get_sun_power(months=6, days=steps / 24))
    sim = Simulator(steps=steps, grid=grid, name='test', extern=False)
    sim.run()
    sim.plot()
