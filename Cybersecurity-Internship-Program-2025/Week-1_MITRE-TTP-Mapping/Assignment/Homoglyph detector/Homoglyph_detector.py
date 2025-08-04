# homoglyph_detector.py

homoglyph_map = {
    'а': 'a',  # Cyrillic a
    'Α': 'A',  # Greek Alpha
    'А': 'A',  # Cyrillic A
    'à': 'a', 'á': 'a', 'â': 'a', 'ä': 'a', 'ã': 'a', 'å': 'a',
    'е': 'e',  # Cyrillic e
    'Ε': 'E',  # Greek Epsilon
    'Е': 'E',  # Cyrillic E
    'і': 'i',  # Cyrillic i
    'Ι': 'I',  # Greek Iota
    'І': 'I',  # Cyrillic I
    'ο': 'o',  # Greek Omicron
    'О': 'O',  # Cyrillic O
    'о': 'o',  # Cyrillic o (lowercase)
    '0': 'o',  # zero digit often used as o
    'с': 'c',  # Cyrillic c
    'С': 'C',  # Cyrillic C
    'р': 'p',  # Cyrillic p
    'Р': 'P',  # Cyrillic P
    'ѡ': 'w',  # Cyrillic w
    'ԝ': 'w',  # Cyrillic w alternative
    'ԛ': 'q',  # Cyrillic q alternative
    'ϙ': 'q',  # Greek q alternative
    'Ԍ': 'G',  # Cyrillic G
    'ɢ': 'g',  # Latin g small capital
    'ɡ': 'g',  # Latin script small g
    'l': 'l',
    '1': 'l',  # digit 1 often replaced for letter l
    'í': 'i', 'ì': 'i', 'ï': 'i', 'î': 'i',
    'ß': 'b',
    # Add more mappings if needed
}

def normalize_homoglyphs(text):
    return ''.join(homoglyph_map.get(c, c) for c in text)

def detect_homoglyphs(base, candidates):
    base_norm = normalize_homoglyphs(base.lower())
    matches = []
    for c in candidates:
        # Skip exact matches
        if c.lower() == base.lower():
            continue
        if normalize_homoglyphs(c.lower()) == base_norm:
            matches.append(c)
    return matches

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python homoglyph_detector.py <base_domain> <domain_list.txt>")
        sys.exit(1)

    base_domain = sys.argv[1]
    domain_file = sys.argv[2]

    try:
        with open(domain_file, 'r', encoding='utf-8') as f:
            domains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ File not found: {domain_file}")
        sys.exit(1)

    results = detect_homoglyphs(base_domain, domains)

    print(f"\n🔍 Base Domain: {base_domain}")
    if results:
        print("⚠️ Homoglyphs Detected:")
        for match in results:
            print(" -", match)
    else:
        print("✅ No homoglyphs detected.")
