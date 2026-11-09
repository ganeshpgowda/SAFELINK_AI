"""SafeLink AI - Synthetic and Curated Training Dataset Generator.

Generates a balanced, realistic, and diverse dataset of legitimate and
fraudulent URLs covering smishing, phishing, typosquatting, credential theft,
as well as authentic modern web patterns.
"""

import random
from typing import List, Tuple
import pandas as pd

from backend.feature_extractor import extract_features, FEATURE_COLUMNS


def get_legitimate_urls() -> List[str]:
    """Generates a diverse set of legitimate URLs across domains, paths, and schemes."""
    base_domains = [
        "https://www.google.com/search?q=cybersecurity+best+practices",
        "https://en.wikipedia.org/wiki/Phishing",
        "https://github.com/torvalds/linux/blob/master/README.md",
        "https://stackoverflow.com/questions/5212870/how-to-extract-features-from-url",
        "https://docs.python.org/3/library/urllib.parse.html",
        "https://www.amazon.com/dp/B08N5WRWNW/ref=syn_sd_onsite_desktop",
        "https://www.apple.com/iphone-16-pro/specs/",
        "https://www.microsoft.com/en-us/software-download/windows11",
        "https://www.netflix.com/browse/genre/839338",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://medium.com/@infosec_daily/understanding-url-structure-7c8a",
        "https://www.nytimes.com/section/technology",
        "https://www.bbc.co.uk/news/technology-68192843",
        "https://pypi.org/project/scikit-learn/#history",
        "https://fastapi.tiangolo.com/tutorial/bigger-applications/",
        "https://streamlit.io/gallery",
        "https://www.linkedin.com/in/cyber-analyst-profile",
        "https://www.reddit.com/r/netsec/comments/url_reputation_models/",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview",
        "https://www.cloudflare.com/learning/security/what-is-phishing/",
        "https://chase.com/personal/banking",
        "https://www.paypal.com/us/home",
        "https://www.bankofamerica.com/credit-cards/",
        "https://stripe.com/docs/api",
        "https://aws.amazon.com/s3/pricing/",
        "https://cloud.google.com/bigquery/docs/quickstarts",
        "https://www.harvard.edu/programs/computer-science",
        "https://www.mit.edu/research/",
        "https://www.cisa.gov/cybersecurity-best-practices",
        "https://www.nih.gov/news-events/news-releases",
        "https://www.nature.com/articles/s41586-024-001",
        "https://www.economist.com/finance-and-economics",
        "https://news.ycombinator.com/item?id=3912048",
        "https://www.spotify.com/us/premium/",
        "https://store.steampowered.com/app/1091500/Cyberpunk_2077/",
        "https://www.target.com/p/apple-airpods-pro-2/-/A-867",
        "https://www.bestbuy.com/site/laptop-computers/all-laptops/",
        "https://www.booking.com/hotel/fr/paris-central.en-gb.html",
        "https://www.airbnb.com/rooms/104829104",
        "https://www.uber.com/ride/",
        "https://web.whatsapp.com/",
        "https://telegram.org/apps",
        "https://discord.com/channels/@me",
        "https://slack.com/pricing",
        "https://zoom.us/join",
        "https://www.coursera.org/specializations/machine-learning",
        "https://edx.org/course/introduction-to-computer-science",
        "https://arxiv.org/abs/2301.00001",
        "https://huggingface.co/models",
        "https://kaggle.com/datasets"
    ]

    legit_variants = []
    # Seed base domains
    legit_variants.extend(base_domains)

    # Generate synthetic realistic legitimate variations
    common_roots = [
        "techcrunch", "theverge", "forbes", "bloomberg", "reuters", "sciencedirect",
        "springer", "wiley", "ieee", "acm", "salesforce", "atlassian", "gitlab",
        "bitbucket", "trello", "notion", "figma", "canva", "zendesk", "shopify",
        "hubspot", "mailchimp", "docker", "kubernetes", "elastic", "mongodb"
    ]
    tlds = ["com", "org", "net", "io", "co", "dev", "app", "edu", "gov", "co.uk", "de", "in"]
    paths = [
        "about-us", "contact", "pricing", "features", "solutions/enterprise",
        "blog/2026/03/product-release", "documentation/v2/api", "help/getting-started",
        "careers/openings", "privacy-policy", "terms-of-service", "resources/whitepaper"
    ]
    queries = [
        "", "?src=newsletter", "?utm_source=twitter&utm_medium=social",
        "?page=2&sort=recent", "?category=cloud&lang=en", "?ref=homepage"
    ]

    for root in common_roots:
        for _ in range(40):
            tld = random.choice(tlds)
            path = random.choice(paths)
            q = random.choice(queries)
            sub = random.choice(["", "www.", "blog.", "docs.", "api.", "app."])
            scheme = random.choice(["https://", "https://", "https://", "http://"])
            url = f"{scheme}{sub}{root}.{tld}/{path}{q}"
            legit_variants.append(url)

    return legit_variants


def get_fraudulent_urls() -> List[str]:
    """Generates a diverse set of fraudulent/phishing URLs covering multiple attack vectors."""
    fraud_urls = []

    # 1. IP-based Phishing URLs
    ip_templates = [
        "http://{ip}/login/chase-online.php",
        "http://{ip}/verify-account/paypal/signin.html",
        "http://{ip}/apple-id/update-billing.php?session={sess}",
        "http://{ip}:8080/secure/bankofamerica/auth",
        "http://{ip}/netflix-payment/failed-update.html",
        "http://{ip}/whatsapp-lottery/claim-reward.php",
        "http://{ip}/telegram/airdrop/claim_bonus",
        "http://{ip}/binance/kyc-verification/login.php?ref=sms"
    ]
    for _ in range(250):
        ip = f"{random.randint(11, 215)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
        sess = f"{random.randint(100000, 999999)}"
        template = random.choice(ip_templates)
        fraud_urls.append(template.format(ip=ip, sess=sess))

    # 2. Brand Spoofing / Subdomain Deception
    brands = ["paypal", "apple", "chase", "netflix", "microsoft", "amazon", "google", "binance", "wells-fargo", "whatsapp"]
    suspicious_tlds = ["xyz", "top", "work", "loan", "click", "club", "buzz", "cf", "tk", "ml", "gq", "icu", "fit"]
    deceptive_prefixes = [
        "secure-login", "account-verification", "billing-update", "security-alert",
        "auth-portal", "resolution-center", "password-reset", "unusual-activity"
    ]

    for brand in brands:
        for _ in range(40):
            tld = random.choice(suspicious_tlds)
            prefix = random.choice(deceptive_prefixes)
            rand_suffix = f"{random.randint(10, 99)}"
            url = f"http://{brand}.com.{prefix}-{rand_suffix}.{tld}/signin?redirect=auth"
            fraud_urls.append(url)
            
            url2 = f"https://{prefix}-{brand}-customer-service.{tld}/verify.php?user_id=auth"
            fraud_urls.append(url2)

    # 3. Typosquatting
    typos = [
        "paypa1.com.security-help.xyz", "paypai-login.club", "apple-id-supp0rt.top",
        "micros0ft-office365-verify.xyz", "amaz0n-prime-reward.top", "netfl1x-billing.loan",
        "chase-bank-alert.xyz", "wellsfarg0-online.work", "whaatsapp-bonus.buzz",
        "faceb00k-security-notice.icu", "instagraam-badge-verify.top"
    ]
    for typo in typos:
        for _ in range(20):
            scheme = random.choice(["http://", "https://"])
            sub = random.choice(["verify.", "account.", "secure.", "login.", "auth."])
            param = f"?token={random.randint(10000, 99999)}&action=urgent"
            fraud_urls.append(f"{scheme}{sub}{typo}/index.php{param}")

    # 4. WhatsApp / SMS Lottery, Gift, and Crypto Scams (Smishing)
    scam_hooks = [
        "free-iphone-winner", "whatsapp-gold-edition-download", "crypto-airdrop-bonus-500",
        "instant-personal-loan-approved", "tax-refund-gov-alert", "unclaimed-lottery-prize",
        "electricity-bill-unpaid-urgent-disconnect", "kyc-update-pan-aadhaar-link",
        "bank-account-blocked-verify-now", "fedex-delivery-failed-fee-payment"
    ]
    for hook in scam_hooks:
        for _ in range(25):
            tld = random.choice(suspicious_tlds)
            rand_num = random.randint(100, 999)
            fraud_urls.append(f"http://{hook}-{rand_num}.{tld}/claim?ref=sms_msg")
            fraud_urls.append(f"https://{hook}.service-portal{rand_num}.xyz/pay?amount=2.50")

    # 5. '@' Credential Masking Tricks
    at_targets = [
        "http://www.google.com@evil-phishing-host.xyz/login.html",
        "http://www.paypal.com@185.220.101.5/verify",
        "https://www.apple.com@account-security-update.top/auth",
        "http://www.chase.com@portal-verify-account.click/signon"
    ]
    for at_url in at_targets:
        for _ in range(25):
            fraud_urls.append(at_url + f"?ref={random.randint(1000, 9999)}")

    # 6. Punycode Spoofing
    puny_templates = [
        "http://xn--pypal-4qa.com/login",
        "http://xn--gogle-qqa.com/verify-account",
        "http://xn--appl-coa.com/support/id",
        "http://xn--chse-q5a.com/online-banking"
    ]
    for p_url in puny_templates:
        for _ in range(25):
            fraud_urls.append(p_url + f"?session={random.randint(100, 999)}")

    # 7. Shortened URLs masked with fraud parameters
    shorteners = ["bit.ly", "tinyurl.com", "is.gd", "cutt.ly", "rb.gy"]
    for s in shorteners:
        for _ in range(30):
            fraud_urls.append(f"http://{s}/urgent-bank-verify-{random.randint(10, 99)}")
            fraud_urls.append(f"https://{s}/free-crypto-giveaway-{random.randint(100, 999)}")

    # 8. High-Entropy Machine Generated Domains (DGA)
    for _ in range(150):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        dga_host = "".join(random.choices(chars, k=random.randint(16, 26)))
        tld = random.choice(suspicious_tlds)
        fraud_urls.append(f"http://{dga_host}.{tld}/gate.php?id={random.randint(1000, 9999)}")

    return fraud_urls


def build_dataset() -> pd.DataFrame:
    """Builds and labels the feature dataset from legitimate and fraud URLs."""
    print("Generating legitimate URL corpus...")
    legit_urls = get_legitimate_urls()
    print(f"Generated {len(legit_urls)} legitimate URLs.")

    print("Generating fraud/phishing URL corpus...")
    fraud_urls = get_fraudulent_urls()
    print(f"Generated {len(fraud_urls)} fraud URLs.")

    data_rows = []

    # Process legitimate samples (label = 0)
    for url in legit_urls:
        try:
            res = extract_features(url)
            row = res["features"]
            row["url"] = url
            row["is_fraud"] = 0
            data_rows.append(row)
        except Exception as e:
            continue

    # Process fraudulent samples (label = 1)
    for url in fraud_urls:
        try:
            res = extract_features(url)
            row = res["features"]
            row["url"] = url
            row["is_fraud"] = 1
            data_rows.append(row)
        except Exception as e:
            continue

    df = pd.DataFrame(data_rows)
    # Shuffle dataset
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    print(f"Total dataset created: {len(df)} samples ({df['is_fraud'].value_counts().to_dict()})")
    return df


if __name__ == "__main__":
    df = build_dataset()
    from backend.config import DATASET_PATH
    DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATASET_PATH, index=False)
    print(f"Dataset successfully saved to {DATASET_PATH}")

