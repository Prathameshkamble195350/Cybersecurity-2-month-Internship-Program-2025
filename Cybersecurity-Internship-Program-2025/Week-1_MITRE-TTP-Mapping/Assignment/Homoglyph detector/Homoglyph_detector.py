import unicodedata
import difflib

homoglyph_map = {
    'а': 'a', 'А': 'A',
    'е': 'e', 'Е': 'E',
    'о': 'o', 'О': 'O',
    'і': 'i', 'І': 'I',
    'р': 'p', 'Р': 'P',
    'с': 'c', 'С': 'C',
    'Ь': 'b', 'ʏ': 'y',
    'ʟ': 'l', 'ꜰ': 'f',
    'ᴋ': 'k'
}

whitelist = [
    'google.com', 'facebook.com', 'youtube.com', 'amazon.com',
    'yahoo.com', 'wikipedia.org', 'twitter.com', 'instagram.com',
    'linkedin.com', 'netflix.com', 'microsoft.com', 'apple.com',
    'paypal.com', 'reddit.com', 'whatsapp.com', 'zoom.us',
    'tiktok.com', 'bing.com', 'github.com', 'stackoverflow.com'
]

def normalize(text):
    return ''.join(homoglyph_map.get(c, c) for c in text)

def is_suspicious(domain, whitelist):
    norm_domain = normalize(domain)
    close = difflib.get_close_matches(norm_domain, whitelist, cutoff=0.8)
    return norm_domain, close

if __name__ == "__main__":
    domain = input("Enter domain: ")
    normalized, matches = is_suspicious(domain, whitelist)
    print(f"Normalized: {normalized}")
    if matches:
        print("⚠️ Suspicious! Looks similar to:", matches)
    else:
        print("✅ Domain appears safe.")
