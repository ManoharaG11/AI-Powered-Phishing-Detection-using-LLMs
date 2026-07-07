# utils/sender_check.py
import csv
import os
import re
import dns.resolver
from typing import Optional

ROOT = os.path.dirname(__file__)  # utils/
PROJECT_ROOT = os.path.dirname(ROOT)
SENDER_CSV = os.path.join(PROJECT_ROOT, "data", "sender_list.csv")

def load_blacklist():
    bad = set()
    if not os.path.exists(SENDER_CSV):
        return bad
    with open(SENDER_CSV, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            bad.add(row[0].strip().lower())
    return bad

def check_mx_record(domain: str) -> bool:
    """
    Return True if MX record exists for domain
    """
    try:
        answers = dns.resolver.resolve(domain, 'MX', lifetime=5)
        return len(answers) > 0
    except Exception:
        return False

def extract_ip_from_header(raw_header: str) -> Optional[str]:
    """
    Find first IPv4 address in 'Received:' header lines if present.
    """
    if not raw_header:
        return None
    # Look for Received: ... (123.45.67.89) or [123.45.67.89]
    matches = re.findall(r'\[?(\d{1,3}(?:\.\d{1,3}){3})\]?', raw_header)
    if matches:
        # return the last (closest to sender) or first? choose first appearance
        return matches[0]
    return None

def analyze_sender(sender_email: str, raw_header: str = "") -> dict:
    """
    Returns a dict with sender analysis
    """
    domain = ""
    if sender_email and "@" in sender_email:
        domain = sender_email.split("@")[-1].lower().strip()

    blacklist = load_blacklist()
    is_blacklisted = domain in blacklist

    mx_exists = False
    if domain:
        mx_exists = check_mx_record(domain)

    extracted_ip = extract_ip_from_header(raw_header)

    # simple heuristics for suspicious local-part
    local_part = sender_email.split("@")[0] if "@" in sender_email else ""
    suspicious_local = False
    if re.search(r'\d{4,}', local_part) or len(local_part) < 3:
        suspicious_local = True

    report = {
        "sender_email": sender_email,
        "domain": domain,
        "blacklisted": is_blacklisted,
        "mx_record_exists": mx_exists,
        "suspicious_local_part": suspicious_local,
        "extracted_ip": extracted_ip
    }
    return report
