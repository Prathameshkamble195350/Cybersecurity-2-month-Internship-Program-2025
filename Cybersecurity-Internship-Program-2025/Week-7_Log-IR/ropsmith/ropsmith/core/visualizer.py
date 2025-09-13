import matplotlib.pyplot as plt
import networkx as nx

def visualize(graph):
    nx.draw(graph, with_labels=True, node_size=1500, node_color="lightblue")
    plt.show()
