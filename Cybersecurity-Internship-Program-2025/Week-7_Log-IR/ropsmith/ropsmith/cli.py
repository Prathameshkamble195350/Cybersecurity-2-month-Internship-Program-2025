import argparse
from .banner import print_banner
from .core import loader, disasm, gadget_finder, graph_builder, chain_hypotheses

def main():
    parser = argparse.ArgumentParser(description="ROPSmith: ROP Chain Exploration Tool")
    parser.add_argument("binary", help="Path to ELF binary")
    args = parser.parse_args()

    print_banner()
    binary = loader.load_binary(args.binary)
    print(f"[+] Loaded binary: {binary['path']} ({binary['arch']})")

    insns = disasm.disassemble(binary)
    gadgets = gadget_finder.find_gadgets(insns)
    graph = graph_builder.build_graph(gadgets)
    chains = chain_hypotheses.generate(graph)

    print("\n[+] Found Gadgets:")
    for g in gadgets[:10]:
        print("   ->", g)

    print("\n[+] Example Hypotheses:")
    for c in chains[:3]:
        print("   ->", " -> ".join(c))

if __name__ == "__main__":
    main()
