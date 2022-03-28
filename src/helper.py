from matplotlib import pyplot as plt
from pyvis.network import Network

from src.Nodes.consumer import Consumer
from src.Nodes.extern import Extern
from src.Nodes.generators.grids.simple_grids import SimpleGrid
from src.Nodes.producer import Producer
from src.Nodes.storage import Storage
from src.examples.prosumer import draw_grid

grid = SimpleGrid(steps=12, number_producer=0, number_consumer=0, transportation_eff=0.9)
consumer = Consumer([500, 1500, 2000, 900, 2500, 300, 3000, 400, 1000, 1500, 1000, 700])
grid.adding_node(consumer, .9)
producer = Producer([1500, 2500, 3000, 1400, 1500, 0, 0, 700, 1000, 3000, 1500, 500])
grid.adding_node(producer, 0.9)
extern = Extern(12)
grid.adding_node(extern, 1)

grid.run_simulation()

steps = range(12)
fig, axs = plt.subplots(2, 2)
axs[0, 0].plot([-e for e in extern.sold_per_step], label='without storage')
axs[0, 0].set_title('extern')

axs[1, 0].plot(producer.sold_per_step)
axs[1, 0].set_title('supply and demand')

axs[1, 0].plot(consumer.bought_per_step)

draw_grid(5, grid, 'without_battery')

battary = Storage(12, capacity=1000, load=500)
grid.adding_node(battary, 1)
extern.clear()
grid.run_simulation()
axs[0, 0].plot([-e for e in extern.sold_per_step], label='c=1000,l =500')

axs[0, 1].plot(steps, battary.sold_per_step, steps, battary.load_per_step[0:12])
axs[0, 1].set_title('storage load and balance c =1000,l =500')
draw_grid(5, grid, 'with_battey c = 1000, l=500')

grid2 = SimpleGrid(steps=12, number_producer=0, number_consumer=0, transportation_eff=0.9)
grid2.adding_node(consumer, .9)
grid2.adding_node(producer, 0.9)
grid2.adding_node(extern, 1)
storage2 = Storage(steps=12, capacity=3000, load=500)
grid2.adding_node(storage2, 1)
extern.clear()
grid2.run_simulation()
axs[0, 0].plot([-e for e in extern.sold_per_step], label='c=3000,l =500')
axs[0, 0].legend(loc='lower right')
axs[1, 1].plot(steps, storage2.sold_per_step, steps, storage2.load_per_step[0:12])
axs[1, 1].set_title('storage load and balance c 3000,l =500')
draw_grid(5, grid, 'with_battey c = 3000, l=500')
plt.show()
