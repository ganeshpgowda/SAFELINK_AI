"""Unit tests for SafeLink AI heuristic security rules.
"""

from backend.feature_extractor import extract_features
from backend.heuristics import evaluate_heuristics


def test_ip_address_heuristic():
    url = "http://192.168.1.100/login/bank.html"
    extracted = extract_features(url)
    score, factors, recs = evaluate_heuristics(extracted["features"], extracted["anatomy"])
    
    assert score >= 35
    codes = [f.code for f in factors]
    assert "IP_AS_HOSTNAME" in codes
    assert any(r.priority == "critical" for r in recs)


def test_brand_spoofing_heuristic():
    url = "http://paypal.com.verify-account.xyz/login"
    extracted = extract_features(url)
    score, factors, recs = evaluate_heuristics(extracted["features"], extracted["anatomy"])

    assert score >= 40
    codes = [f.code for f in factors]
    assert "BRAND_IMPERSONATION" in codes


def test_at_symbol_heuristic():
    url = "http://www.google.com@evil-site.com/login"
    extracted = extract_features(url)
    score, factors, recs = evaluate_heuristics(extracted["features"], extracted["anatomy"])

    codes = [f.code for f in factors]
    assert "AT_SYMBOL_OBFUSCATION" in codes


def test_clean_legitimate_url_heuristic():
    url = "https://www.google.com/search?q=machine+learning"
    extracted = extract_features(url)
    score, factors, recs = evaluate_heuristics(extracted["features"], extracted["anatomy"])

    # Clean site should have 0 or very low heuristic score
    assert score <= 10
    categories = [f.category for f in factors]
    assert "safety" in categories

