"""SafeLink AI - Website Intention & Threat Objective Analyzer.

Analyzes URL lexical components, deceptive patterns, query parameters, and typosquatting
to identify the primary objective and targeted user data of the website.
"""

from typing import Dict, Any, List, Optional


def analyze_website_intention(
    url: str,
    anatomy: Dict[str, Any],
    features: Dict[str, Any],
    typosquatting: Dict[str, Any],
    risk_score: int
) -> Dict[str, Any]:
    """Determines the primary intention and threat objective of the submitted link.
    
    Returns structured details including category, intent summary, targeted data,
    and attack strategy.
    """
    clean_url = url.lower()
    netloc = anatomy.get("netloc", "").lower()
    path = anatomy.get("path", "").lower()
    query = anatomy.get("query", "").lower()
    root_domain = anatomy.get("root_domain", "").lower()
    keywords = anatomy.get("keyword_matches", [])
    search_space = f"{netloc} {path} {query}"

    is_typo = typosquatting.get("is_typosquatting", False)
    target_brand = typosquatting.get("target_brand")
    official_domain = typosquatting.get("official_domain")
    is_official = typosquatting.get("is_official_brand", False)

    # 1. LEGITIMATE PLATFORMS (Low Risk & Verified Official)
    if is_official or (risk_score <= 30 and not is_typo):
        if "search" in path or "q=" in query or root_domain in ["google", "bing", "duckduckgo", "yahoo"]:
            return {
                "category": "Web Search & Information Retrieval",
                "intent_summary": "The link is an authentic search query on a recognized search engine intended to retrieve web results.",
                "targeted_data": ["None (Standard Search Query)"],
                "attack_strategy": "Legitimate / Non-Malicious",
                "risk_context": "Safe",
                "safe_alternative": None
            }
        elif root_domain in ["github", "gitlab", "stackoverflow", "pypi", "python", "docs"]:
            return {
                "category": "Developer & Software Resource",
                "intent_summary": "Authentic developer platform or open-source repository for technical documentation, code collaboration, or libraries.",
                "targeted_data": ["None (Public Developer Resource)"],
                "attack_strategy": "Legitimate / Non-Malicious",
                "risk_context": "Safe",
                "safe_alternative": None
            }
        elif root_domain in ["wikipedia", "medium", "nytimes", "bbc", "nature", "arxiv", "edu"]:
            return {
                "category": "Informational & Reference Resource",
                "intent_summary": "Public educational, encyclopedia, or news reference article for standard information consumption.",
                "targeted_data": ["None (Public Content)"],
                "attack_strategy": "Legitimate / Non-Malicious",
                "risk_context": "Safe",
                "safe_alternative": None
            }
        else:
            brand_label = target_brand if target_brand else root_domain.capitalize()
            return {
                "category": f"Official Service ({brand_label})",
                "intent_summary": f"Authentic official website for {brand_label}. No deceptive, spoofing, or fraudulent indicators were found.",
                "targeted_data": ["None (Legitimate Service)"],
                "attack_strategy": "Legitimate / Non-Malicious",
                "risk_context": "Safe",
                "safe_alternative": None
            }

    # 2. MALICIOUS / FRAUDULENT INTENTIONS (High / Medium Risk)

    # A. Cryptocurrency / Web3 Wallet Drainer
    crypto_terms = ["crypto", "wallet", "airdrop", "binance", "coinbase", "metamask", "phantom", "trustwallet", "seed", "token", "bitcoin", "eth"]
    if any(t in search_space for t in crypto_terms):
        brand_str = f"impersonating {target_brand}" if is_typo else "operating a crypto scam"
        return {
            "category": "Cryptocurrency Theft & Wallet Draining",
            "intent_summary": (
                f"The primary goal of this link is {brand_str} to trick users into connecting Web3 wallets, "
                "surrendering 12/24-word seed recovery phrases, or authorizing malicious contract approvals to drain digital assets."
            ),
            "targeted_data": [
                "Secret Recovery Passphrases (Seed Words)",
                "Private Wallet Keys",
                "Web3 Smart Contract Permissions",
                "Cryptocurrency Account Logins"
            ],
            "attack_strategy": "Lure of free airdrops, fake staking yields, or urgent wallet security updates.",
            "risk_context": "Critical Threat",
            "safe_alternative": f"Access crypto platforms only via their official verified domains or hardware wallets."
        }

    # B. Financial Fraud & Banking Credential Theft
    banking_terms = ["bank", "chase", "paypal", "wellsfargo", "bankofamerica", "citi", "billing", "wire", "invoice", "payroll", "tax-refund", "refund"]
    if any(t in search_space for t in banking_terms) or (is_typo and target_brand in ["PayPal", "Chase Bank", "Wells Fargo", "Bank of America", "Citibank"]):
        brand_name = target_brand if target_brand else "financial institutions"
        return {
            "category": "Financial Fraud & Banking Theft",
            "intent_summary": (
                f"This website is designed to harvest online banking credentials and payment card details "
                f"by imitating {brand_name}. Its purpose is unauthorized money transfers and financial theft."
            ),
            "targeted_data": [
                "Online Banking Usernames & Passwords",
                "Credit / Debit Card Numbers (PAN, CVV, Expiry)",
                "One-Time Passwords (OTP) & SMS Verification Codes",
                "Account PINs & Security Questions"
            ],
            "attack_strategy": "Fake login/billing forms and payment failure alerts to harvest banking credentials.",
            "risk_context": "Critical Threat",
            "safe_alternative": f"Log in only via your official banking app or by typing the exact official URL ({official_domain if official_domain else 'official bank website'})."
        }

    # C. Prize, Lottery, & WhatsApp Smishing Scam
    lottery_terms = ["lottery", "winner", "claim", "prize", "gift", "iphone", "bonus", "reward", "free"]
    if any(t in search_space for t in lottery_terms):
        return {
            "category": "Lottery & Gift Scam (Smishing Lure)",
            "intent_summary": (
                "The intention is to exploit social engineering and greed by claiming you won an unearned prize, "
                "gift card, or iPhone. Victims are tricked into paying 'shipping fees' or sharing personal identity data."
            ),
            "targeted_data": [
                "Credit Card Numbers (under the guise of 'shipping/delivery' fees)",
                "Full Name, Residential Address & Phone Numbers",
                "WhatsApp / Social Media Contacts (for viral propagation)"
            ],
            "attack_strategy": "Smishing (SMS/messaging lure) exploiting fake urgency and unearned prize announcements.",
            "risk_context": "High Threat",
            "safe_alternative": "Ignore and delete the message. Legitimate companies never give expensive electronics via random links."
        }

    # D. Account Suspension & Urgency Coercion
    urgent_terms = ["suspend", "suspended", "limited", "action-required", "urgent", "unlock", "alert", "notice", "unusual"]
    if any(t in search_space for t in urgent_terms):
        brand_str = f"your {target_brand} account" if target_brand else "your online account"
        return {
            "category": "Coercive Account Hijacking (Fear / Urgency)",
            "intent_summary": (
                f"The intention of this site is to create artificial panic claiming {brand_str} is 'suspended' "
                "or 'compromised', coercing you to urgently submit your login credentials before you have time to verify the sender."
            ),
            "targeted_data": [
                "Account Passwords",
                "Password Reset Tokens",
                "Email Addresses & Phone Numbers",
                "Two-Factor Authentication Backup Codes"
            ],
            "attack_strategy": "Psychological intimidation through false threats of immediate account termination.",
            "risk_context": "High Threat",
            "safe_alternative": f"Check your account status directly inside the official app, never through links in unsolicited alerts."
        }

    # E. Credential Harvesting & Corporate Login Theft
    login_terms = ["login", "signin", "auth", "verify", "verification", "password", "security", "portal", "account", "office365", "outlook"]
    if any(t in search_space for t in login_terms) or is_typo:
        impersonated = target_brand if target_brand else "trusted services"
        return {
            "category": "Credential Harvesting / Account Hijacking",
            "intent_summary": (
                f"The primary intention is to steal usernames, emails, and passwords by displaying a cloned login page "
                f"imitating {impersonated} (e.g. {typosquatting.get('technique', 'deceptive domain name')})."
            ),
            "targeted_data": [
                "Login Usernames & Email Addresses",
                "Account Passwords",
                "Multi-Factor Authentication (MFA/2FA) Codes",
                "Session Cookies & Auth Tokens"
            ],
            "attack_strategy": "Deceptive clone of an authentication portal designed to capture credentials silently.",
            "risk_context": "Critical Threat",
            "safe_alternative": f"Go to the authentic portal at https://{official_domain if official_domain else 'the official service website'}."
        }

    # F. KYC / Identity Document Theft
    kyc_terms = ["kyc", "pan", "aadhaar", "ssn", "identity", "id-verify", "passport", "doc"]
    if any(t in search_space for t in kyc_terms):
        return {
            "category": "Identity Theft & Document Harvesting (KYC Fraud)",
            "intent_summary": (
                "The site aims to collect government identity cards, tax identifiers (SSN/PAN/Aadhaar), and photos "
                "to commit financial identity fraud or create synthetic identity accounts."
            ),
            "targeted_data": [
                "Government ID Numbers (SSN, National ID, PAN, Aadhaar)",
                "Passport / Driver's License Scans",
                "Biometric Photos / Selfies",
                "Full Date of Birth and Mother's Maiden Name"
            ],
            "attack_strategy": "Fictitious compliance or mandatory account re-verification warning.",
            "risk_context": "Critical Threat",
            "safe_alternative": "Submit identity documents only through verified official mobile apps or physical bank branches."
        }

    # G. Destination Concealment (URL Shortener)
    if features.get("is_shortened") == 1:
        return {
            "category": "Destination Concealment / Link Masking",
            "intent_summary": (
                "The intent of this link is to hide the actual landing page domain from your sight and bypass spam scanners. "
                "It redirects you to an undisclosed secondary destination."
            ),
            "targeted_data": [
                "Hidden Destination (Requires Link Expansion)",
                "Device Fingerprinting / Click Tracking Data"
            ],
            "attack_strategy": "Link shortener masking to prevent users from inspecting the actual domain before clicking.",
            "risk_context": "Medium Risk",
            "safe_alternative": "Use a link unshortener or preview tool to verify the destination domain before opening."
        }

    # H. General Suspicious Site
    return {
        "category": "Suspicious / Unverified Web Activity",
        "intent_summary": (
            "The link exhibits multiple anomalous patterns (such as unusual character entropy, non-standard structure, "
            "or disposable domains) often associated with spam campaigns or untrusted landing pages."
        ),
        "targeted_data": [
            "User Traffic & Ad Clicks",
            "Potential Tracking Fingerprints"
        ],
        "attack_strategy": "Disposability and domain evasion techniques.",
        "risk_context": "Medium / Warning",
        "safe_alternative": "Exercise caution. Do not download files or input confidential information."
    }

