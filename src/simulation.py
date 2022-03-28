import timeit

import matplotlib.pyplot as plt
import numpy as np
from pyvis.network import Network

from src.Nodes.generators.grids.city import get_city, get_green_city, add_capacity, remove_capacity
from src.Nodes.generators.producer.solar_producer import get_sun_power
from src.Nodes.generators.producer.wind_producer import get_random_wind_velocities
from src.Nodes.grid import Grid, AllData
from src.graph import grid_to_graph


class Simulator:
    def __init__(self, grid: Grid, steps: int, name: str, extern: False):
        self.grid = grid
        self.steps = steps
        self.data = AllData([0] * steps, [0] * steps, [0] * steps, [0] * steps, [0] * steps, [0] * steps,
                            [0] * steps, [0] * steps)
        self.extern = extern
        self.name = name

    def run(self):
        print("Simulator is running")
        start = timeit.timeit()
        self.grid.run_simulation()
        end = timeit.timeit()
        print("Simulation finished, time : " + str(end - start))

        print("collecting data")
        self.data = self.grid.extract_data()

    def graph(self, step, extra=""):
        g = Network(height=1024, width=1024, directed=True)
        grid_to_graph(grid2=self.grid, step=step, network=g)
        g.barnes_hut()
        g.show_buttons()
        g.show(self.name + extra + str(step) + '.html')

    def plot(self, number=1, name=''):
        x = range(self.steps)

        battery_loading = [-load if load < 0 else 0 for load in self.data.balance_battery]
        total_consumption = [battery_loading[i] + self.data.bought[i] for i in x]
        fig, (ax_demand, ax_supply, ax_storage, ax_ex, ax_bar) = plt.subplots(5, 1)
        fig.suptitle(name)
        ax_demand.plot(x, self.data.demand, label='demand')
        ax_demand.plot(x, self.data.bought, label='bought')
        ax_demand.plot(x, battery_loading, label='battery')
        ax_demand.plot(x, total_consumption, label='total')
        ax_demand.set_ylabel('Wh')
        ax_demand.set_title('demand consumer')
        ax_demand.legend()

        battery_supply = [load if load > 0 else 0 for load in self.data.balance_battery]
        total_sold = [battery_supply[i] + self.data.bought[i] for i in x]

        ax_supply.plot(x, self.data.supply, label='supply')
        ax_supply.plot(x, self.data.sold, label='sold')
        ax_supply.plot(x, battery_supply, label='battary')
        ax_supply.plot(x, total_sold, label='total')
        ax_supply.set_ylabel('Wh')
        ax_supply.legend()
        ax_supply.set_title('supply')

        ax_storage.plot(x, self.data.capacity, label='capacity')
        ax_storage.plot(x, self.data.load, label='load')
        ax_storage.plot(x, self.data.balance_battery, label='balance')
        ax_storage.legend()
        ax_storage.set_title('capacyties')
        ax_storage.set_ylabel('Wh')
        ax_demand.plot()

        ax_ex.plot(x, self.data.balance_extern, label='extern')
        ax_ex.legend()
        ax_ex.set_title('extern')
        ax_ex.set_ylabel('Wh')

        demand_met = sum(self.data.bought) / sum(self.data.demand)
        loss = []
        energy_used = sum(self.data.bought) / sum(self.data.supply)
        for i in range(len(self.data.bought)):
            loss.append(total_sold[i] - total_consumption[i])

        loss_rel = sum(loss) / sum(total_sold)
        ax_bar.bar([0, 1], [demand_met, energy_used], label='demand_met, energy_used')
        print(name + " demand met:" + str(demand_met) + ", enegy_used: " + str(energy_used))
        ax_bar.legend()
        plt.show()

    def clear(self):
        self.grid.clear()


if __name__ == "__main__":
    steps = 24
    grid = get_green_city(steps=steps, number=5, wind=get_random_wind_velocities(steps),
                          sun=get_sun_power(months=6, days=steps / 24))
    sim = Simulator(steps=steps, grid=grid, name='test', extern=False)

    sim.run()
    sim.graph(1)
    sim.plot(name='without')
    sim.clear()

    add_capacity(steps, city=grid,
                 level=1, capacity=1000000)
    sim.run()
    name = 'with battery level1 c= 1000000'
    sim.graph(1, name)
    sim.plot(number=2, name=name)
    sim.clear()
    remove_capacity(grid)

    add_capacity(steps, city=grid,
                 level=2, capacity=1000000)
    sim.run()
    name = 'with battery level2 c= 1000000'
    sim.graph(1, name)
    sim.plot(number=2, name=name)
    sim.clear()
    remove_capacity(grid)

    plt.show()
