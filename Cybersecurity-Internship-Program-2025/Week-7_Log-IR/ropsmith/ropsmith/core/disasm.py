from capstone import Cs, CS_ARCH_X86, CS_MODE_64

def disassemble(binary):
    # Fake byte sequence for demo
    code = b"\x90\x90\xc3"  # nop; nop; ret
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    return list(md.disasm(code, 0x1000))
