from models import *
import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

tree = BSTtree([])

tree.root = Node(10)
tree.root.left = Node(20, tree.root)
tree.root.left.left = Node(30, tree.root.left)
tree.root.left.left.left = Node(40, tree.root.left.left)

tree._LL(tree.root.left)

tree.list_nodes()
edges = tree.edges
labels = tree.nodes


G = nx.Graph()
G.add_edges_from(edges)
pos = nx.nx_agraph.graphviz_layout(G, prog = 'dot')


fig = plt.figure()
nx.draw(G,pos,labels = labels,with_labels = True, font_color = 'black', node_size = 1200, edge_color = 'grey', node_color = 'white')
fig.set_facecolor('black')
plt.show()