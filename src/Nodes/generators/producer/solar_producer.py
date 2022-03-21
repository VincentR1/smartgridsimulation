from src.Nodes.producer import Producer
import math

SUN_POWER_BERLIN_AVR_MONTH = [2890, 3800, 4800, 5780, 5900, 6120, 6620, 6190, 5730, 4230, 3250, 2630]
SUN_AVARAGE_DAWN_BERLIN_PER_MONTH = [8, 7.33, 6.33, 6.166, 5.166, 4.66, 5, 5.83, 6.66, 7.5, 7.5, 8.166]


class SolarProducer(Producer):
    def __init__(self, sun_hight, max_watts=200, efficency=0.14, qm=1):
        suppl_per_step = [qm * sun * efficency if sun * efficency < max_watts else max_watts for sun in sun_hight]
        super().__init__(supply_per_step=suppl_per_step)


def get_sun_power(sunrises=SUN_AVARAGE_DAWN_BERLIN_PER_MONTH, sun_noons=[12] * 12,
                  avarage_sun_power=SUN_AVARAGE_DAWN_BERLIN_PER_MONTH, steps_per_day=24, days=1, months=4):
    sig = (sun_noons[months] - sunrises[months]) / 3
    sig2 = sig ** 2
    e = sun_noons[months]
    sun_per_day = [0] * steps_per_day
    for step in range(steps_per_day):
        sun_per_day[step] = avarage_sun_power[months] * 1 / math.sqrt(2 * math.pi * sig2) * math.exp(
            -(step - e) ** 2 / (2 * sig2))
    sun = sun_per_day * days
    return sun
