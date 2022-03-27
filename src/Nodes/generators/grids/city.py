import random

from src.Nodes.generators.consumer.simple_consumers import RandomConsumer
from src.Nodes.generators.producer.solar_producer import get_sun_power, SolarProducer
from src.Nodes.generators.producer.wind_producer import WindTurbineProducer, get_random_wind_velocities
from src.Nodes.grid import Grid
import config


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
    dist = Grid(steps, [get_green_street(steps, number=random.randint(5, 25), sun=sun) for i in range(number)],
                [.97] * number)
    for i in range(random.randint(0, 3)):
        dist.adding_node(WindTurbineProducer(wind, powercurve=config.PC_ALSTOM_ECO122_2700), .97)
    qm = random.randint(0, 10)

    if qm:
        dist.adding_node(SolarProducer(sun_hight=sun, max_watts=350, qm=1000 * qm), .97)
    return dist


def get_green_city(steps: int, number, wind, sun):
    city = Grid(steps,
                [get_green_district(steps, number=random.randint(3, 7), wind=wind, sun=sun) for i in range(number)],
                [.97] * number)
    city.adding_node(WindTurbineProducer(wind_velocity=wind), 0.9)
    city.adding_node(WindTurbineProducer(wind_velocity=wind), 0.9)
    return city
