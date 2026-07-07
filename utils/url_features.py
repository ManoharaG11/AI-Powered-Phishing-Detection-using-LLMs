# utils/url_features.py
import re
from urllib.parse import urlparse

SHORTENERS = [
    "bit.ly","tinyurl.com","t.co","goo.gl","ow.ly","buff.ly","adf.ly",
]

def has_ip_address(url: str) -> bool:
    if not url:
        return False
    # find patterns like 123.123.123.123
    return bool(re.search(r'(\d{1,3}\.){3}\d{1,3}', url))

def is_shortened(url: str) -> bool:
    if not url:
        return False
    try:
        domain = urlparse(url).netloc.lower()
        for s in SHORTENERS:
            if s in domain:
                return True
        return False
    except Exception:
        return False

def count_dots(url: str) -> int:
    if not url:
        return 0
    return url.count('.')

def uses_https(url: str) -> bool:
    return url.startswith("https://")

def url_length(url: str) -> int:
    return len(url) if url else 0

def url_score_heuristic(url: str) -> float:
    """
    Basic heuristic scoring for URL suspiciousness (0..1)
    Higher = more suspicious
    """
    if not url:
        return 0.0
    score = 0.0
    if has_ip_address(url):
        score += 0.4
    if is_shortened(url):
        score += 0.25
    if count_dots(url) > 5:
        score += 0.15
    if not uses_https(url):
        score += 0.15
    if url_length(url) > 100:
        score += 0.05
    return min(score, 1.0)

def url_to_text_features(url: str) -> str:
    """
    Convert some url features into a short textual token string so TF-IDF can pick them up.
    Eg: 'HAS_IP SHORTENED MANY_DOTS NO_HTTPS LONG_URL'
    """
    tokens = []
    if not url:
        return ""
    if has_ip_address(url):
        tokens.append("HAS_IP")
    if is_shortened(url):
        tokens.append("SHORTENED")
    if count_dots(url) > 3:
        tokens.append("MANY_DOTS")
    if not uses_https(url):
        tokens.append("NO_HTTPS")
    if url_length(url) > 80:
        tokens.append("LONG_URL")
    return " ".join(tokens)
