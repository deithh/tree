from models import *
import networkx as nx
import matplotlib.pyplot as plt

array = [i for i in range(35)]
tree = AVLtree(array)

tree.delete(7)
tree.delete(11)
tree.delete(12)
tree.delete(13)

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
