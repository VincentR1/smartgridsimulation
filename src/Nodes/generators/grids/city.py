import random

from src.Nodes.generators.consumer.simple_consumers import RandomConsumer, Fabric
from src.Nodes.generators.producer.solar_producer import get_sun_power, SolarProducer
from src.Nodes.generators.producer.wind_producer import WindTurbineProducer, get_random_wind_velocities
from src.Nodes.grid import Grid
import config
from src.Nodes.node import Node
from src.Nodes.storage import Storage


def get_city(steps: int, number=5):
    city = Grid(steps, [get_district(steps, number=random.randint(3, 7)) for i in range(number)], [.97] * number)
    return city


def get_street(steps: int, number=10):
    houses = [RandomConsumer(steps=steps, value=random.randint(2800, 6000)) for i in range(number)]
    return Grid(steps, houses, [.98] * number)


def get_district(steps: int, number=10):
    return Grid(steps, [get_street(steps, number=random.randint(5, 25)) for i in range(number)], [.97] * number)


def get_green_street(steps, number, sun):
    houses = [RandomConsumer(steps=steps, value=random.randint(2800, 6000)) for i in range(number)]
    street = Grid(steps, houses, [.98] * number)
    qm = random.randint(0, 10)

    if qm:
        street.adding_node(SolarProducer(sun_hight=sun, max_watts=350, qm=10 * qm), .97)
    return street


def get_green_district(steps, number, wind, sun):
    dist = Grid(steps, [get_green_street(steps, number=random.randint(25, 90), sun=sun) for i in range(number)],
                [.97] * number)
    for i in range(random.randint(0, 1)):
        dist.adding_node(Fabric(steps=steps, value=random.randint(40000, 50000)), .98)
    for i in range(random.randint(0, 1)):
        dist.adding_node(WindTurbineProducer(wind, powercurve=config.PC_ALSTOM_ECO122_2700), .97)
    qm = random.randint(0, 5)

    if qm:
        dist.adding_node(SolarProducer(sun_hight=sun, max_watts=350, qm=1000 * qm), .97)
    return dist


def get_green_city(steps: int, number, wind, sun):
    city = Grid(steps,
                [get_green_district(steps, number=random.randint(3, 7), wind=wind, sun=sun) for i in range(number)],
                [.97] * number)
    city.adding_node(WindTurbineProducer(wind_velocity=wind), 0.9)
    city.adding_node(WindTurbineProducer(wind_velocity=wind), 0.9)

    city.adding_node(WindTurbineProducer(wind_velocity=wind), 0.9)
    return city


def add_capacity(steps, city: Node, level, capacity):
    i = level
    if i == 0:
        city.adding_node(Storage(steps=steps, capacity=capacity, load=0), .98)
    else:
        nodes = [node for node in city.nodes if isinstance(node, Grid)]
        c = capacity / len(nodes)
        for n in nodes:
            add_capacity(steps, n, i - 1, c)


def remove_capacity(city: Node):
    if isinstance(city, Grid):
        new_nodes = []
        new_eff = []
        for i in range(len(city.nodes)):
            node = city.nodes[i]
            if not isinstance(node, Storage):
                new_nodes.append(node)
                new_eff.append(city.transport_efficiencies[i])
                if isinstance(node, Grid):
                    remove_capacity(node)

        city.nodes = new_nodes
        city.transport_efficiencies = new_eff
