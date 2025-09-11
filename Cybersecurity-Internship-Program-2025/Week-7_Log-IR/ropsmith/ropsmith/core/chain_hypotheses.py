def generate(graph):
    chains = []
    nodes = list(graph.nodes)
    for i in range(min(3, len(nodes)-2)):
        chains.append(nodes[i:i+3])
    return chains
