"""SafeLink AI - Configuration and Security Signatures.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "rf_model.joblib"
DATASET_PATH = BASE_DIR / "backend" / "training" / "dataset.csv"

# Risk Thresholds
LOW_RISK_MAX = 30
MEDIUM_RISK_MAX = 69
# High Risk is >= 70

# Suspicious / High-Abuse Top-Level Domains (TLDs)
# Often used due to free registration, lenient abuse policies, or cheap pricing
SUSPICIOUS_TLDS = {
    "xyz", "top", "work", "loan", "click", "tk", "ml", "ga", "cf", "gq",
    "fit", "buzz", "rest", "bid", "country", "kim", "racing", "surf",
    "stream", "date", "download", "accountant", "faith", "review", "trade",
    "party", "science", "space", "win", "vip", "icu", "cam", "link",
    "monster", "tokyo", "bar", "men", "club"
}

# Standard Legitimate Generic & Country TLDs
LEGITIMATE_COMMON_TLDS = {
    "com", "org", "net", "edu", "gov", "mil", "io", "co", "uk", "ca",
    "de", "fr", "au", "in", "jp", "cn", "br", "nl", "se", "no", "ch",
    "app", "dev", "ai", "tech"
}

# Known URL Shortener Domains
KNOWN_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "buff.ly",
    "adf.ly", "bit.do", "cutt.ly", "rb.gy", "shorte.st", "t2m.io", "s.id",
    "qr.ae", "cli.re", "tiny.cc", "v.gd", "bl.ink", "lnkd.in"
}

# High-Profile Brand Names Frequently Targeted in Phishing / Smishing
TARGETED_BRANDS = [
    "paypal", "google", "apple", "microsoft", "amazon", "netflix",
    "facebook", "instagram", "whatsapp", "telegram", "chase", "wellsfargo",
    "bankofamerica", "citibank", "binance", "coinbase", "dropbox", "yahoo",
    "linkedin", "twitter", "ebay", "walmart", "spotify", "steam", "adobe",
    "roblox", "meta", "icloud", "outlook", "office365", "gmail"
]

# Sensitive / Urgency / Phishing Keywords
SUSPICIOUS_KEYWORDS = [
    "login", "signin", "verify", "verification", "secure", "security",
    "account", "update", "banking", "wallet", "claim", "bonus", "gift",
    "free", "reward", "kyc", "support", "billing", "confirm", "password",
    "authenticate", "unusual", "suspend", "suspended", "limited", "reset",
    "refund", "crypto", "prize", "lottery", "winner", "urgent", "unlock",
    "authenticate", "validation", "alert", "notice", "action-required",
    "wire", "payroll", "tax-refund"
]

# Common ports that are standard for web traffic
STANDARD_PORTS = {80, 443}

# Model and Hybrid Weighting
# Model contributes 55%, Heuristics contribute 45% to final risk score
WEIGHT_ML = 0.55
WEIGHT_HEURISTICS = 0.45

