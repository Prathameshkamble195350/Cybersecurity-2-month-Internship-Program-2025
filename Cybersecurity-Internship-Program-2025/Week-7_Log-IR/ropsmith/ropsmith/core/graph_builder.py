import networkx as nx

def build_graph(gadgets):
    G = nx.DiGraph()
    for g in gadgets:
        G.add_node(g)
    # demo: link sequentially
    for i in range(len(gadgets)-1):
        G.add_edge(gadgets[i], gadgets[i+1])
    return G
