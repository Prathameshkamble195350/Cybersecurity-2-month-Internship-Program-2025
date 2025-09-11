def find_gadgets(insns):
    gadgets = []
    for i in insns:
        if i.mnemonic == "ret":
            gadgets.append(f"0x{i.address:x}: {i.mnemonic} {i.op_str}")
    return gadgets
