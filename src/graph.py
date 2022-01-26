import networkx as nx
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

H = nx.Graph()
##Draws random node positions with (no. of nodes, no. of connection for each nodes)
G = nx.barabasi_albert_graph(20, 1)

H1 = "House 1"
H2 = "House 2"
H3 = "House 3"
H.add_node(1,pos=(1,1))
H.add_node(2, pos=(1,2))
H.add_node(3, pos=(2,2))

H.add_node(H1, pos=(4,3))
H.add_edge(1,2)
H.add_edge(1,H1)
pos = nx.get_node_attributes(H, 'pos')
#H.add_nodes_from([(2,3),(4,6)])
#H.add_nodes_from([(4, {"color": "red"}), (5, {"color", "green"})]) ##NOT WORK YET
nx.draw(H,pos,with_labels=True);
plt.show()
nx.draw_networkx(G, with_labels=True)
plt.show()

'''
G = nx.petersen_graph()
subax1 = plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
subax2 = plt.subplot(122)
nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show()
'''
