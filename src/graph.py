from pyvis.network import Network

from src.Nodes.consumer import Consumer
from src.Nodes.extern import Extern
from src.Nodes.generators.grids.simple_grids import SimpleGrid
from src.Nodes.generators.producer.simple_producers import SimpleProducer
from src.Nodes.grid import Grid
from src.Nodes.node import Node
from src.Nodes.producer import Producer
from src.Nodes.storage import Storage


def grid_to_graph(grid2: Node, step, network, prev=0, i=0, ):
    if isinstance(grid2, Extern):
        node = 'e' + str(i)
        value = grid2.sold_per_step[step]
        network.add_node(node, label='e', title='input:' + str(value))

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


def get_demand_result(step: int, grid: Node):
    demand = 0
    if isinstance(grid, Grid):
        for n in grid.nodes:
            demand += get_demand_result(step, n)
    elif isinstance(grid, Consumer):
        demand = grid.demand_per_step[step]

    return demand


def get_production_result(step: int, grid: Node):
    demand = 0
    if isinstance(grid, Grid):
        for n in grid.nodes:
            demand += get_production_result(step, n)
    elif isinstance(grid, Producer):
        demand = grid.supply_per_step[step]

    return demand
