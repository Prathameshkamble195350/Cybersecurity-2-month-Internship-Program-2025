import networkx as nx
import matplotlib.pyplot as plt

def visualize_gadgets(gadgets, output_file="rop_graph.png"):
    """
    Visualize ROP gadgets and chains using NetworkX.
    gadgets: list of tuples like (address, "instruction sequence")
    """
    G = nx.DiGraph()

    # Add nodes
    for addr, instr in gadgets:
        G.add_node(f"{hex(addr)}\n{instr}")

    # Add dummy edges (linear chain for example)
    for i in range(len(gadgets) - 1):
        G.add_edge(
            f"{hex(gadgets[i][0])}\n{gadgets[i][1]}",
            f"{hex(gadgets[i+1][0])}\n{gadgets[i+1][1]}"
        )

    # Draw
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)  # nicer layout
    nx.draw(
        G, pos,
        with_labels=True,
        node_size=2500,
        node_color="red",
        font_size=8,
        font_color="white",
        edge_color="gray",
        arrows=True,
    )
    plt.title("ROPSmith Gadget Graph", fontsize=14)
    plt.savefig(output_file, dpi=300)
    print(f"[+] ROP graph saved to {output_file}")
