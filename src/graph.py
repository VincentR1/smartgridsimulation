import networkx as nx
#G = nx.graph()
import matplotlib.pyplot as plt
from PIL import Image
#plt.interactive(False)

G = nx.petersen_graph()

subax1 = plt.subplot(121)

nx.draw(G, with_labels=True, font_weight='bold')

subax2 = plt.subplot(122)

nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show()
plt.show(block = True)
