# ROPSmith

**ROPSmith** is a Return-Oriented Programming (ROP) chain exploration tool.  
It analyzes binaries, finds gadgets, builds gadget graphs, and proposes *human-readable* hypotheses of possible chains.  

⚠️ This tool is for **educational and research purposes only**. It does **not** generate live exploits.  

## Features
- Binary loader (ELF metadata only)
- Capstone disassembly wrappers
- Gadget discovery
- Graph model of gadgets
- Hypothetical chain construction (no payloads)
- CLI with red ACCSI banner
- Optional Flask-based web UI (for visualization)

## Usage
```bash
python3 -m ropsmith.cli ./examples/toy_binary
