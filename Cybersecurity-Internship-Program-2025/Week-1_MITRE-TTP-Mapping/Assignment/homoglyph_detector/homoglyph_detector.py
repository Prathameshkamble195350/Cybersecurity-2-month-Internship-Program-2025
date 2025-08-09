import difflib
import unicodedata
from utils.homoglyph_map import homoglyph_map

# Step 1: Normalize domain using custom homoglyph map and Unicode normalization
def normalize_domain(domain):
    replaced = ''.join(homoglyph_map.get(c, c) for c in domain)
    normalized = unicodedata.normalize("NFKC", replaced)
    return normalized

# Step 2: Check against whitelist
def is_suspicious(input_domain, whitelist):
    normalized = normalize_domain(input_domain)
    matches = difflib.get_close_matches(normalized, whitelist, n=1, cutoff=0.9)
    return normalized != input_domain, matches, normalized

def main():
    whitelist = [
        "google.com",
        "facebook.com",
        "youtube.com",
        "twitter.com",
        "instagram.com"
    ]

    user_input = input("Enter a domain name to check: ").strip().lower()

    altered, matches, normalized = is_suspicious(user_input, whitelist)

    print(f"\nOriginal:   {user_input}")
    print(f"Normalized: {normalized}")

    if altered and matches:
        print(f"⚠️  Suspicious! Looks like: {matches[0]}")
    elif altered and not matches:
        print("⚠️  Suspicious characters used, but doesn't match any known domain.")
    else:
        print("✅ Safe. No suspicious characters or homoglyphs detected.")

if __name__ == "__main__":
    main()
