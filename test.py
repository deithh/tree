from models import *
import networkx as nx
import matplotlib.pyplot as plt

array = [1, 2, 3, 4, 5, 6, 7, 8, 9]
np.random.shuffle(array)
tree = BSTtree(array)
# tree.delete(1)


tree.list_nodes()
edges = tree.edges
labels = tree.nodes

G = nx.Graph()
G.add_edges_from(edges)
pos = nx.nx_agraph.graphviz_layout(G, prog='dot')

fig = plt.figure()
nx.draw(G, pos, labels=labels, with_labels=True, font_color='black', node_size=1200, edge_color='grey',
        node_color='white')
fig.set_facecolor('black')
plt.show()
