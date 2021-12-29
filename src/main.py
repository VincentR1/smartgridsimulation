from src.grid import Grid
from src.simulation import Simulation


def main():
    steps = 100
    simulation = Simulation(Grid(steps), steps)
    simulation.run()


if __name__ == "__main__":
    main()
