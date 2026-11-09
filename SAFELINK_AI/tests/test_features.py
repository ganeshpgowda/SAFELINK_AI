"""Unit tests for SafeLink AI URL feature extraction and parsing.
"""

import pytest
from backend.feature_extractor import (
    calculate_shannon_entropy,
    is_ip_address,
    parse_domain_parts,
    check_brand_spoofing,
    extract_features,
    normalize_url,
    FEATURE_COLUMNS,
)


def test_shannon_entropy():
    # Empty string has 0 entropy
    assert calculate_shannon_entropy("") == 0.0
    # Repeating string has low entropy
    assert calculate_shannon_entropy("aaaaaaa") == 0.0
    # Random characters have higher entropy
    h1 = calculate_shannon_entropy("google")
    h2 = calculate_shannon_entropy("a98sdf71kjn3qwxz")
    assert h2 > h1


def test_is_ip_address():
    assert is_ip_address("192.168.1.1") is True
    assert is_ip_address("10.0.0.1:8080") is True
    assert is_ip_address("google.com") is False
    assert is_ip_address("192.168.1.300") is False  # Invalid IP


def test_parse_domain_parts():
    # Standard domain
    sub, root, tld = parse_domain_parts("www.google.com")
    assert sub == "www"
    assert root == "google"
    assert tld == "com"

    # Multi-level ccTLD
    sub, root, tld = parse_domain_parts("portal.service.co.uk")
    assert sub == "portal"
    assert root == "service"
    assert tld == "co.uk"

    # Deep subdomains
    sub, root, tld = parse_domain_parts("a.b.c.target.org")
    assert sub == "a.b.c"
    assert root == "target"
    assert tld == "org"


def test_check_brand_spoofing():
    # Brand in subdomain but root domain is evil.xyz
    is_spoofed, brand = check_brand_spoofing(
        root_domain="evil", subdomain="paypal.com.login", path=""
    )
    assert is_spoofed is True
    assert "paypal" in brand

    # Legitimate root domain
    is_spoofed, brand = check_brand_spoofing(
        root_domain="paypal", subdomain="www", path="/myaccount"
    )
    assert is_spoofed is False

    # Typosquatting in root domain
    is_spoofed, brand = check_brand_spoofing(
        root_domain="paypa1", subdomain="", path=""
    )
    assert is_spoofed is True
    assert "paypal" in brand


def test_extract_features_completeness():
    test_url = "https://secure-login.paypal.com.account-update.xyz/verify?user=test"
    res = extract_features(test_url)
    assert "features" in res
    assert "anatomy" in res
    assert "normalized_url" in res

    feats = res["features"]
    for col in FEATURE_COLUMNS:
        assert col in feats, f"Missing feature column: {col}"

    assert feats["is_https"] == 1
    assert feats["suspicious_tld"] == 1  # .xyz
    assert feats["brand_spoofing_detected"] == 1  # paypal in subdomain while root is account-update

