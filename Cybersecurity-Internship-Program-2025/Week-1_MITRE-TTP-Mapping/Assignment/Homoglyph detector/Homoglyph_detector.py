# homoglyph_detector.py

import unicodedata

# Manual homoglyph mapping
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
    'í': 'i', 'ì': 'i', 'ï': 'i', 'î': 'i',
    'ο': 'o',  # Greek Omicron
    'О': 'O',  # Cyrillic O
    'о': 'o',  # Cyrillic o (lowercase)
    '0': 'o',  # zero digit
    'с': 'c',  # Cyrillic c
    'С': 'C',  # Cyrillic C
    'р': 'p',  # Cyrillic p
    'Р': 'P',  # Cyrillic P
    'ѡ': 'w',  # Cyrillic w
    'ԝ': 'w',  # Cyrillic w
    'ԛ': 'q',  # Cyrillic q
    'ϙ': 'q',  # Greek q
    'Ԍ': 'G',  # Cyrillic G
    'ɢ': 'g',  # Latin small capital G
    'ɡ': 'g',  # Script small g
    'l': 'l',
    '1': 'l',  # digit 1 for letter l
    'ß': 'b',
    # Add more mappings as needed
}

def normalize_homoglyphs(text):
    # Step 1: Unicode normalization to decompose diacritics
    text = unicodedata.normalize('NFKD', text)

    # Step 2: Remove diacritical marks
    text = ''.join(c for c in text if not unicodedata.combining(c))

    # Step 3: Apply manual homoglyph map
    return ''.join(homoglyph_map.get(c, c) for c in text)

def detect_homoglyphs(base, candidates):
    base_norm = normalize_homoglyphs(base.lower())
    matches = []
    for c in candidates:
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