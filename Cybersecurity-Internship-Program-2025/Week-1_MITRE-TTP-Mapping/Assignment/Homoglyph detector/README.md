# 🕵️‍♂️ Homoglyph Detection Tool

This Python-based tool detects **homoglyphs** (visually similar characters) in domain names. It is designed to identify phishing or typosquatting attacks by comparing a base domain to a list of suspicious domains, using a **character-by-character mapping** of common Unicode homoglyphs.

## 📌 Features

- Detects visually deceptive domain names (e.g., `gооgle.com`, `gοοgle.com`)
- Custom homoglyph mapping (Cyrillic, Greek, Latin, digits)
- Works offline and runs in **Termux** or any Python environment
- Lightweight, fast, and open source

## 📦 Requirements

- Python 3
- unicodedata and difflib libraries

### 📲 Install in Termux:
```bash
pkg update
pkg install python git
