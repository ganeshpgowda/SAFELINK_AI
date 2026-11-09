"""SafeLink AI - Interactive CLI Demonstration & Verification.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.model_service import model_service

DEMO_URLS = [
    ("http://nnicrosoft.com/login", "Typosquatting: 'nnicrosoft' vs 'microsoft'"),
    ("http://g00gle.com/search?q=test", "Typosquatting: 'g00gle' vs 'google'"),
    ("https://www.google.com/search?q=cybersecurity", "Legitimate Official Google"),
    ("https://www.microsoft.com/en-us", "Legitimate Official Microsoft"),
    ("http://non-existent-fake-domain-12345.xyz/login", "Domain Existence Check: Non-Existent (NXDOMAIN)"),
    ("http://192.168.1.150:8080/bankofamerica/auth/login.php", "Raw IP Phishing Link"),
    ("http://claim-free-iphone16-winner.gift-rewards.top/claim", "WhatsApp Smishing Lottery"),
]


def run_cli_demo():
    print("\n" + "=" * 80)
    print("       🛡️  SAFELINK AI – FRAUD URL DETECTOR CLI VERIFICATION")
    print("       Tagline: Don't click blindly. Check before you trust.")
    print("=" * 80 + "\n")

    for url, desc in DEMO_URLS:
        print(f"Analyzing [{desc}]:")
        print(f"URL: {url}")
        res = model_service.analyze(url)
        risk = res.risk
        dns = res.domain_existence
        typo = res.typosquatting

        phish_badge = "🚨 PHISHING" if risk.is_phishing else ("🟡 SUSPICIOUS" if risk.risk_level == "Medium" else "✅ LEGITIMATE")
        score_grade = f"{risk.score_grade} ({risk.score}/100)"
        exists_str = "✅ Active / Resolves" if dns.exists else "❌ Non-Existent (NXDOMAIN)"

        print(f"1. Phishing Verdict:   {phish_badge} ({risk.phishing_classification})")
        print(f"2. Risk Score & Grade: {score_grade}")
        print(f"3. Domain Existence:   {exists_str} (Status: {dns.status})")
        
        if typo.is_typosquatting:
            print(f"4. Brand Similarity:   🚨 MIMICS '{typo.target_brand}' ({typo.similarity_percentage:.0f}% match, {typo.technique})")
            print(f"   Official Domain:    https://{typo.official_domain}")
        elif typo.is_official_brand:
            print(f"4. Brand Similarity:   🛡️ VERIFIED OFFICIAL '{typo.target_brand}' DOMAIN")
        else:
            print(f"4. Brand Similarity:   No brand lookalike detected")

        intent = res.intention
        print(f"5. Main Intention:     🎯 {intent.category} ({intent.risk_context})")
        print(f"   Objective:          {intent.intent_summary}")
        print(f"   Targeted Data:      {', '.join(intent.targeted_data)}")

        print(f"Summary Verdict:       {risk.verdict}")
        print("-" * 80)


if __name__ == "__main__":
    run_cli_demo()
