"""Unit tests for SafeLink AI Typosquatting and Similarity Engine.
"""

from backend.typosquatting import (
    analyze_typosquatting,
    damerau_levenshtein_distance,
    normalize_visual_substitutions
)


def test_damerau_levenshtein():
    # Identical
    assert damerau_levenshtein_distance("google", "google") == 0
    # Omission
    assert damerau_levenshtein_distance("micosoft", "microsoft") == 1
    # Transposition
    assert damerau_levenshtein_distance("googel", "google") == 1
    # Substitution
    assert damerau_levenshtein_distance("googly", "google") == 1


def test_visual_substitutions():
    norm, techs = normalize_visual_substitutions("nnicrosoft")
    assert norm == "microsoft"
    assert any("nn" in t for t in techs)

    norm, techs = normalize_visual_substitutions("g00gle")
    assert norm == "google"
    assert any("0" in t for t in techs)

    norm, techs = normalize_visual_substitutions("paypa1")
    assert norm == "paypal"


def test_analyze_typosquatting_nnicrosoft():
    res = analyze_typosquatting(root_domain="nnicrosoft", full_netloc="nnicrosoft.com")
    assert res["is_typosquatting"] is True
    assert res["target_brand"] == "Microsoft"
    assert res["official_domain"] == "microsoft.com"
    assert "nn" in res["technique"]


def test_analyze_typosquatting_g00gle():
    res = analyze_typosquatting(root_domain="g00gle", full_netloc="g00gle.com")
    assert res["is_typosquatting"] is True
    assert res["target_brand"] == "Google"
    assert res["official_domain"] == "google.com"


def test_analyze_official_microsoft():
    res = analyze_typosquatting(root_domain="microsoft", full_netloc="www.microsoft.com")
    assert res["is_typosquatting"] is False
    assert res["is_official_brand"] is True
    assert res["target_brand"] == "Microsoft"


def test_analyze_official_google():
    res = analyze_typosquatting(root_domain="google", full_netloc="www.google.com")
    assert res["is_typosquatting"] is False
    assert res["is_official_brand"] is True
    assert res["target_brand"] == "Google"


def test_analyze_tld_squatting():
    res = analyze_typosquatting(root_domain="google", full_netloc="google.xyz")
    assert res["is_typosquatting"] is True
    assert res["target_brand"] == "Google"
    assert "TLD-Squatting" in res["technique"]


def test_analyze_subdomain_spoofing():
    res = analyze_typosquatting(root_domain="attacker", full_netloc="microsoft.com.attacker.xyz")
    assert res["is_typosquatting"] is True
    assert res["target_brand"] == "Microsoft"
    assert "Subdomain" in res["technique"]


def test_analyze_bare_brand():
    res = analyze_typosquatting(root_domain="microsoft", full_netloc="microsoft")
    assert res["is_typosquatting"] is False
    assert res["is_official_brand"] is True
    assert res["target_brand"] == "Microsoft"

