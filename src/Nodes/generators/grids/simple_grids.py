from src.Nodes.generators.consumer.simple_consumers import SimpleConsumer
from src.Nodes.generators.producer.simple_producers import SimpleProducer
from src.Nodes.grid import Grid


class SimpleGrid(Grid):
    def __init__(self, number_consumer=10, number_producer=1, steps=1, transportation_eff=.8):
        consumers = [
            SimpleConsumer(steps) for i in range(number_consumer)]
        producers = [SimpleProducer(steps, value=5) for i in range(number_producer)]
        nodes = consumers + producers
        transportation_effs = [transportation_eff] * len(nodes)
        transportation_effs[3] = .7
        super().__init__(steps, nodes, transportation_effs)
