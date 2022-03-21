from matplotlib import pyplot as plt
from pyvis.network import Network

from src.Nodes.extern import Extern
from src.Nodes.generators.consumer.simple_consumers import RandomSwitchingConsumer
from src.Nodes.generators.producer.solar_producer import get_sun_power, SolarProducer, SUN_POWER_BERLIN_AVR_MONTH
from src.Nodes.grid import Grid
from src.Nodes.node import Node
from src.Nodes.storage import Storage
from src.graph import grid_to_graph, get_demand_result, get_production_result


def get_Single_House_Posumer(steps, qm=4, month=6):
    singleHouse = RandomSwitchingConsumer(steps=steps, value=1000)

    power = get_sun_power(days=int(steps / 25), avarage_sun_power=SUN_POWER_BERLIN_AVR_MONTH,
                          steps_per_day=25, months=month)
    print(power)
    solarCellAugust = SolarProducer(sun_hight=power,
                                    max_watts=200 * qm,
                                    efficency=.24,
                                    qm=qm, )

    return Grid(steps=steps, nodes=[singleHouse, solarCellAugust], transport_efficiencies=[.99, .99])


def draw_grid(steps: int, grid: Node, name: str):
    for step in range(steps):
        g = Network(height=500, width=500, directed=True)
        grid_to_graph(grid2=grid, step=step, network=g)
        g.barnes_hut()
        g.show_buttons()
        g.show(name + str(step) + '.html')


if __name__ == "__main__":
    steps = 100
    month = 8

    monitornode = Extern(steps)
    grid = get_Single_House_Posumer(steps, qm=15, month=6)
    grid.adding_node(monitornode, 1)

    grid.run_simulation()
    draw_grid(steps, grid, 'without_battery')
    fig, axs = plt.subplots(3, 1)
    axs[0].plot([get_demand_result(s, grid) for s in range(steps)])
    axs[0].plot([get_production_result(s, grid) for s in range(steps)])
    axs[1].plot(monitornode.sold_per_step)

    battery = Storage(steps=steps, capacity=20000, load=0)
    grid.adding_node(battery, .9)
    monitornode.clear()

    grid.run_simulation()
    draw_grid(steps, grid, 'without_battery')
    axs[2].plot(battery.sold_per_step)
    axs[2].plot(battery.load)
    axs[1].plot(monitornode.sold_per_step)

    plt.show()
