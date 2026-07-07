# utils/preprocess.py
import re
import html
from urllib.parse import urlparse

def clean_text(text: str) -> str:
    """
    Basic text cleaning:
    - Remove HTML entities
    - Remove URLs (we handle URLs separately)
    - Lowercase and remove extra whitespace
    """
    if not text:
        return ""
    text = html.unescape(text)
    # remove URLs
    text = re.sub(r'http\S+|www\.\S+', ' ', text)
    # remove non-alphanumeric (keep @ . _ -)
    text = re.sub(r'[^0-9a-zA-Z@._\-\s]', ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_domain(email: str) -> str:
    """
    return domain from an email address
    """
    if "@" not in email:
        return ""
    try:
        return email.split("@")[-1].lower().strip()
    except Exception:
        return ""
