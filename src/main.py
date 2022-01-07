from src.Nodes.consumer import Consumer
from src.grid import Grid
from src.simulation import Simulation

import networkx as nx


def main():
    steps = 6
    G = nx.Graph()
    consumers = [Consumer(steps), Consumer(steps), Consumer(steps), Consumer(steps), Consumer(steps), ]
    G.add_nodes_from(consumers)
    print(list(G.nodes))
    nx.draw(G)

    simulation = Simulation(Grid(steps), steps)
    simulation.run()
    simulation.plot()


if __name__ == "__main__":
    main()
