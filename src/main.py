import uuid
import networkx as nx


def main():
    # 1generate Grid
    u = uuid.uuid4()
    print(u)
    graph = nx.Graph()
    graph.add_node(u)

    print(graph)
    # 2run simulation

    # 3plot data


if __name__ == "__main__":
    main()
