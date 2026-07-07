import os
import random
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, "data")
OUT_PATH = os.path.join(DATA_DIR, "phishing_dataset.csv")

FIRST_NAMES = ["John","Maria","David","Sarah","Michael","Emily","Chris","Jessica","Daniel","Sophia"]
LAST_NAMES = ["Smith","Johnson","Brown","Taylor","Anderson","Thomas","Jackson","White","Harris","Martin"]

PHISHING_URLS = [
    # account takeover / credential theft
    "http://secure-login.{t}/login",
    "https://{t}/verify-account",
    "http://account-update.{t}/auth",
    "https://{t}/reset-password",

    # payment / invoice fraud
    "https://{t}/payment-confirm",
    "https://{t}/invoice/confirm",
    "http://secure-payments.{t}/billing",

    # support impersonation
    "https://support.{t}/ticket",
    "http://helpdesk.{t}/verify",

    # malware-style redirect
    "https://{t}/redirect?to=/security",
    "http://{t}/download/secure-update",
]

SAFE_URLS = [
    "https://www.{t}/news",
    "https://{t}/support",
    "https://www.{t}/account",
    "https://{t}/calendar",
    "https://{t}/invoices",
    "https://{t}/dashboard",
    "https://www.{t}/help/article",
]

# Use mixed-looking domains to avoid trivial token matching.
PHISHING_DOMAINS = [
    "secure-payments.net",
    "fakebank.com",
    "login-security.com",
    "verify-now.xyz",
    "account-alerts.top",
    "rapid-reward.club",
    "support-center.icu",
    "secure-verify.org",
    "billing-confirmation.com",
    "trusted-notice.co",
]

SAFE_DOMAINS = [
    "example.com",
    "company.com",
    "newsletter.example.org",
    "cloud-service.net",
    "service-portal.org",
    "account-portal.com",
    "secure-mail.example",
]

PHISH_EMAIL_SNIPPETS = [
    "Your account has been suspended. Click to verify.",
    "Please verify your payment details to avoid service disruption.",
    "We detected unusual activity. Confirm your identity immediately.",
    "Action required: confirm your billing information.",
    "Security alert: your password may have been compromised.",
    "Limited time offer! Update your account to claim reward.",
    "Your invoice is ready. Review and confirm payment.",
    "Urgent: verify your login to prevent account lock.",
    "We noticed a sign-in attempt from a new device. Verify now.",
]

SAFE_EMAIL_SNIPPETS = [
    # Include some overlap words to prevent “perfect” separation.
    "Meeting reminder: Tomorrow at {time}.",
    "Hi {name}, here are your recent updates.",
    "Thank you for your subscription. You can manage preferences anytime.",
    "Your statement is available in your dashboard.",
    "Reminder: your appointment is scheduled for {date}.",
    "We received your request and will respond within {hours} hours.",
    "Account notice: changes to your settings were successful.",
    "Security tip: review your login activity in the dashboard.",
]

RISK_TYPES = [
    "credential_theft",
    "payment_fraud",
    "account_takeover",
    "malicious_link_redirect",
    "support_impersonation",
    "invoice_fraud",
]

PHISHING_WORDS_BY_TYPE = {
    "credential_theft": ["verify", "login", "password reset", "credentials", "sign-in"],
    "payment_fraud": ["payment", "invoice", "billing", "confirm payment", "charge"],
    "account_takeover": ["account", "locked", "unusual activity", "verify identity", "new device"],
    "malicious_link_redirect": ["redirect", "secure update", "download", "review immediately", "claim"],
    "support_impersonation": ["support", "helpdesk", "ticket", "confirm", "customer service"],
    "invoice_fraud": ["invoice", "receipt", "payment details", "confirm", "review"],
}

PHISHING_WORDS = [
    "suspended","security alert","immediately","limited time","reward","compromised","password reset",
    "payment details","action required","account update","unusual activity","confirm identity"
]

SAFE_WORDS = [
    "meeting","reminder","updates","subscription","dashboard","appointment",
    "request","respond","statement","preferences","information","notification",
    "security tip","settings","login activity"
]


def rand_time():
    h = random.randint(8, 18)
    m = random.choice(["00","15","30","45"])
    return f"{h}:{m}"


def rand_date():
    day = random.randint(1, 28)
    month = random.choice(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
    return f"{day} {month}"


def gen_phish_row():
    risk_type = random.choice(RISK_TYPES)
    t = random.choice(PHISHING_DOMAINS)
    template = random.choice(PHISHING_URLS)
    url = template.format(t=t)

    email = random.choice(PHISH_EMAIL_SNIPPETS)

    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    urgency = random.choice(["ASAP","today","within 24 hours","immediately","now"])

    # Mix in risk-type specific tokens + some generic phishing tokens.
    type_words = PHISHING_WORDS_BY_TYPE[risk_type]
    extra = type_words + random.sample(PHISHING_WORDS, k=random.randint(1,3))
    random.shuffle(extra)
    extra = extra[: random.randint(3,6)]

    action = random.choice(["verify","confirm","update","review","secure your account"])

    # Add slight “legit-ish” phrasing sometimes to avoid perfect separation.
    intro = random.choice([
        "Hi",
        "Hello",
        "Dear",
        "Account team:",
    ])
    connector = random.choice([",", ":", " —"])

    email_text = (
        f"{email} {intro} {name}{connector} please {action} {urgency}. "
        + " ".join(extra)
    )

    return email_text, url, "phishing"


def gen_safe_row():
    t = random.choice(SAFE_DOMAINS)
    template = random.choice(SAFE_URLS)
    url = template.format(t=t)

    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

    # Sometimes include mild security/account language (still safe).
    base = random.choice(SAFE_EMAIL_SNIPPETS).format(
        name=name,
        time=rand_time(),
        date=rand_date(),
        hours=random.randint(1,6),
    )

    extra = random.sample(SAFE_WORDS, k=random.randint(2,4))

    prefix = random.choice(["Hi", "Hello", "Dear"])
    email_text = f"{prefix} {name}, {base} " + " ".join(extra)

    # Ensure no URL tokens appear in the email_text (classifier uses URL separately).
    return email_text, url, "safe"


def main(n_rows=6000, phishing_ratio=0.5, seed=42):
    # Note: caller can set phishing_ratio to create real-world imbalance.
    
    random.seed(seed)

    phishing_n = int(n_rows * phishing_ratio)
    safe_n = n_rows - phishing_n

    rows = []
    for _ in range(phishing_n):
        rows.append(gen_phish_row())
    for _ in range(safe_n):
        rows.append(gen_safe_row())

    df = pd.DataFrame(rows, columns=["email_text","url","label"])

    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)

    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"Generated {len(df)} rows -> {OUT_PATH}")


if __name__ == "__main__":
    # Generate a larger, more varied dataset for better real-world-ish testing.
    # Set phishing_ratio to ~0.2 to mimic real-world class imbalance.
    main(n_rows=10000, phishing_ratio=0.2, seed=42)


