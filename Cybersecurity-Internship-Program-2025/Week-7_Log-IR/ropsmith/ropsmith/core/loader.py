def load_binary(path):
    # In real tool: parse ELF headers
    return {
        "path": path,
        "arch": "x86_64",
        "entry": "0x400000"
    }
