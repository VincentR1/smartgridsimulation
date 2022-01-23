from src.Nodes.generators.consumer.simple_consumers import SimpleConsumer
from src.Nodes.generators.producer.simple_producers import SimpleProducer
from src.Nodes.grid import Grid


class SimpleGrid(Grid):
    def __init__(self, number_consumer=1, number_producer=1, steps=1, transportation_eff=0.8):
        consumers = [
            SimpleConsumer(steps) for i in range(number_consumer)]
        producers = [SimpleProducer(steps, value=1) for i in range(number_producer)]
        nodes = consumers + producers
        transportation_effs = [transportation_eff] * len(nodes)
        super().__init__(steps, nodes, transportation_effs)


class SimpleGridWurm(Grid):
    def __init__(self, number_consumer=1, number_producer=1
                 , number_interconecting_grids=1, steps=1,
                 transport_eff=0.8):
        consumers = [
            SimpleConsumer(steps) for i in range(number_consumer)]
        producers = [SimpleProducer(steps, value=1) for i in range(number_producer)]
        producer_grid = Grid(steps, producers, [transport_eff] * len(producers))
        previous_grid = producer_grid
        last_grid = producer_grid
        for i in range(number_interconecting_grids - 1):
            last_grid = Grid(steps, [], [])
            previous_grid.adding_node(last_grid, transport_eff)
            previous_grid = last_grid
        last_grid.adding_node([consumers], [transport_eff] * len(consumers))
        super().__init__(steps, [producer_grid], [1])
