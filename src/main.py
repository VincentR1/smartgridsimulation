from src.Nodes.generators.consumer.simple_consumers import DayOnNightOff
from src.Nodes.generators.grids.simple_grids import SimpleGrid


def main():
    grid = SimpleGrid(steps=1)
    print(grid.start(0))


if __name__ == "__main__":
    main()
