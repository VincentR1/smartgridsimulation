from pyvis.network import Network

from src.Nodes.consumer import Consumer
from src.Nodes.extern import Extern
from src.Nodes.generators.consumer.simple_consumers import RandomSwitchingConsumer
from src.Nodes.generators.producer.simple_producers import SimpleProducer
from src.Nodes.generators.producer.solar_producer import SolarProducer, get_sun_power
from src.Nodes.generators.producer.wind_producer import WindTurbineProducer, get_random_wind_velocities
from src.Nodes.grid import Grid
from src.Nodes.node import Node
from src.Nodes.storage import Storage
from src.graph import grid_to_graph, get_demand_result
import matplotlib.pyplot as plt

show_grid = True
n_consumer = 1000
steps = 10

print('-------simple sim-------')
consumers = [RandomSwitchingConsumer(steps=steps, value=6000) for i in range(n_consumer)]
producer = WindTurbineProducer(get_random_wind_velocities(steps=steps))
print(producer.supply_per_step)

print('-----------------0')
grid = Grid(steps=steps, nodes=consumers + [producer], transport_efficiencies=[.9] * (n_consumer + 1))
extern = Extern(steps=steps)
print('-----------------1')
grid.adding_node(extern, 1)

consumers2 = [RandomSwitchingConsumer(steps=steps, value=3500) for i in range(100)]
producer2 = SolarProducer(sun_hight=get_sun_power(days=40, steps_per_day=25), max_watts=10000000, efficency=.24,
                          qm=10000000)
grid2 = Grid(steps=steps, nodes=consumers2 + [producer2], transport_efficiencies=[0.8] * 101)

grid.adding_node(grid2, 0.7)
grid.run_simulation()
if show_grid:
    for step in range(steps):
        g = Network(height=1024, width=1028, directed=True)
        grid_to_graph(grid2=grid, step=step, network=g)
        g.barnes_hut()
        g.show_buttons()
        g.show('html/simplesim' + str(step) + '.html')

fig, axs = plt.subplots(3, 1)
axs[0].plot([get_demand_result(s, grid) for s in range(steps)])
axs[0].plot(extern.sold_per_step)
axs[0].plot(producer.sold_per_step)
axs[0].plot(producer2.supply_per_step)

battery = Storage(steps=steps, capacity=4000000, load=0)
grid.adding_node(battery, .9)
extern.clear()
grid.run_simulation()
if show_grid:
    for step in range(steps):
        g = Network(height=1024, width=1024, directed=True)
        grid_to_graph(grid2=grid, step=step, network=g)
        g.barnes_hut()
        g.show_buttons()
        g.show('html/simplesim_with_battery' + str(step) + '.html')

axs[1].plot([get_demand_result(s, grid) for s in range(steps)])
axs[1].plot(extern.sold_per_step)
axs[1].plot(producer.sold_per_step)
axs[1].plot(producer2.supply_per_step)
axs[2].plot(battery.sold_per_step)
axs[2].plot(battery.load_per_step)

plt.show()
