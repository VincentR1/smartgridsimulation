from pyvis.network import Network

from src.Nodes.consumer import Consumer
from src.Nodes.generators.grids.simple_grids import SimpleGrid
from src.Nodes.generators.producer.simple_producers import SimpleProducer
from src.Nodes.grid import Grid
from src.Nodes.node import Node
from src.Nodes.producer import Producer
from src.Nodes.storage import Storage


def grid_to_graph(grid2: Node, step, network, prev=0, i=0, ):
    if isinstance(grid2, Grid):
        node = 'g' + str(i)
        value = grid2.local_balances[step]
        network.add_node(node, label='n', title=str(value))

        for n in grid2.nodes:
            i += 1
            grid_to_graph(grid2=n, step=step, network=network, prev=node, i=i)
    elif isinstance(grid2, Producer):
        node = 'P' + str(i)
        value = grid2.sold_per_step[step]
        network.add_node(node, label='p', title="b:" + str(value) + ",c:" + str(grid2.supply_per_step[step]),
                         color="red", value=grid2.supply_per_step[step])
    elif isinstance(grid2, Consumer):
        node = 'C' + str(i)
        value = -grid2.bought_per_step[step]
        demand = grid2.demand_per_step[step]
        network.add_node(node, label='c', title="b:" +
                                                str(value) + ",d:" + str(demand), color="green")
    elif isinstance(grid2, Storage):
        node = 'S' + str(i)
        value = grid2.sold_per_step[step]
        load = grid2.load[step]
        network.add_node(node, label='s',
                         title="b:" + str(value) + ",load:" + str(load) + ",cap:" + str(grid2.capacity), color="pink")
    if prev:
        if value > 0:
            network.add_edge(node, prev, value=value)
        elif value < 0:
            network.add_edge(prev, node, value=-value)


grid = SimpleGrid(number_consumer=100, number_producer=40, steps=2, transportation_eff=.9)
grid.adding_node(Storage(2, 10000, 9800), .9)
grid.adding_node(SimpleProducer(steps=2, value=1000000), .9)
grid.start(0)
grid.start(1)
g = Network(height=2048, width=2048, directed=True)
grid_to_graph(grid, 0, g)
g.barnes_hut()
g.show_buttons()
g.show('test.html')

g = Network(height=2048, width=2048, directed=True)
grid_to_graph(grid, 1, g)
g.barnes_hut()
g.show_buttons()
g.show('test2.html')

g.add_nodes([1, 2, 3], value=[10, 100, 400],
            title=['I am node 1', 'node 2 here', 'and im node 3'],
            x=[21.4, 54.2, 11.2],
            y=[100.2, 23.54, 32.1],
            label=['NODE 1', 'NODE 2', 'NODE 3'],
            color=['#00ff1e', '#162347', '#dd4b39'])
'''
G = nx.petersen_graph()
subax1 = plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
subax2 = plt.subplot(122)
nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show()
'''
