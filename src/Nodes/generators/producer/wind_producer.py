import numpy as np

from config import PC_ENE_E_126_4200MW
from src.Nodes.producer import Producer


class WindTurbineProducer(Producer):
    def __init__(self, wind_velocity, powercurve=PC_ENE_E_126_4200MW):
        suppl_per_step = [powercurve[int(v)] for v in wind_velocity]
        super().__init__(supply_per_step=suppl_per_step)


def get_random_wind_velocities(steps, shape=2.31, average_v=6.6):
    return (average_v * np.random.weibull(a=shape, size=steps)).tolist()
