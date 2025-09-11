import networkx as nx
from ropsmith.core import graph_builder

def test_graph_builder():
    gadgets = ["g1", "g2", "g3"]
    G = graph_builder.build_graph(gadgets)
    assert len(G.nodes) == 3
    assert ("g1","g2") in G.edges
