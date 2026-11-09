"""Unit tests for SafeLink AI model service and risk calculation.
"""

from backend.model_service import model_service


def test_model_loaded():
    assert model_service.is_loaded() is True
    assert model_service.model is not None


def test_analyze_legitimate_url():
    url = "https://www.google.com/search?q=weather"
    res = model_service.analyze(url)
    assert res.risk.risk_level == "Low"
    assert res.risk.score <= 30
    assert res.anatomy.root_domain == "google"
    assert res.anatomy.tld == "com"


def test_analyze_phishing_url():
    url = "http://paypal.com.secure-update-account.xyz/login?ref=sms"
    res = model_service.analyze(url)
    assert res.risk.risk_level == "High"
    assert res.risk.score >= 70
    assert any(f.code == "BRAND_IMPERSONATION" for f in res.factors)


def test_analyze_ip_url():
    url = "http://192.168.1.1:8080/admin/login.php"
    res = model_service.analyze(url)
    assert res.risk.risk_level == "High"
    assert res.risk.score >= 70
    assert any(f.code == "IP_AS_HOSTNAME" for f in res.factors)

