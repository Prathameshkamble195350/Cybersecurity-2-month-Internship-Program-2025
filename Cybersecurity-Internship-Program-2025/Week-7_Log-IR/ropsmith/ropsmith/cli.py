import argparse
from ropsmith.core.loader import load_binary
from ropsmith.core.gadget_finder import find_gadgets
from ropsmith.core.chain_hypotheses import generate_chains
from ropsmith.core.visualizer import visualize_gadgets
from ropsmith.banner import print_banner

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="ROPSmith - ROP Chain Generator")
    parser.add_argument("binary", help="Path to ELF binary")
    parser.add_argument("--graph", action="store_true", help="Generate ROP graph visualization")
    args = parser.parse_args()

    # Load binary
    binary_path = args.binary
    print(f"[+] Loaded binary: {binary_path}")

    # Find gadgets
    gadgets = find_gadgets(binary_path)
    print(f"[+] Found {len(gadgets)} gadgets")

    # Print a few gadget samples
    for g in gadgets[:10]:
        print(f"   -> {hex(g[0])}: {g[1]}")

    # Generate chain hypotheses
    chains = generate_chains(gadgets)
    print("\n[+] Example ROP Chains:")
    for c in chains[:3]:
        print("   -> " + " -> ".join(c))

    # Graph option
    if args.graph:
        print("\n[+] Generating gadget graph...")
        visualize_gadgets(gadgets, "rop_graph.png")
