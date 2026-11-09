"""Unit tests for SafeLink AI Website Intention Analyzer.
"""

from backend.model_service import model_service


def test_intention_credential_harvesting():
    url = "http://nnicrosoft.com/login"
    res = model_service.analyze(url)
    assert res.intention.category == "Credential Harvesting / Account Hijacking"
    assert "Microsoft" in res.intention.intent_summary or "credentials" in res.intention.intent_summary
    assert any("Password" in d for d in res.intention.targeted_data)


def test_intention_banking_theft():
    url = "http://192.168.1.150:8080/bankofamerica/auth/login.php"
    res = model_service.analyze(url)
    assert "Banking" in res.intention.category or "Credential" in res.intention.category
    assert any("Banking" in d or "Password" in d for d in res.intention.targeted_data)


def test_intention_lottery_scam():
    url = "http://claim-free-iphone16-winner.gift-rewards.top/claim"
    res = model_service.analyze(url)
    assert "Lottery" in res.intention.category or "Gift" in res.intention.category
    assert any("Credit Card" in d or "Phone" in d for d in res.intention.targeted_data)


def test_intention_legitimate_search():
    url = "https://www.google.com/search?q=machine+learning"
    res = model_service.analyze(url)
    assert "Search" in res.intention.category
    assert res.intention.risk_context == "Safe"

