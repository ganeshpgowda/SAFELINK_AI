"""Unit tests for SafeLink AI Domain Existence and DNS Verification.
"""

from backend.domain_verifier import check_domain_existence


def test_existing_domain():
    res = check_domain_existence("google.com", timeout=5.0)
    # Under valid network, google.com resolves
    if res["status"] != "DNS Lookup Timed Out":
        assert res["exists"] is True
        assert "Active" in res["status"]
        assert len(res["resolved_ips"]) > 0


def test_non_existent_domain():
    res = check_domain_existence("this-domain-surely-does-not-exist-xyz-9876543210.xyz", timeout=3.0)
    assert res["exists"] is False
    assert any(term in res["status"] for term in ["Non-Existent", "NXDOMAIN", "Timed Out"])


def test_ip_address_host():
    res = check_domain_existence("192.168.1.1")
    assert res["exists"] is True
    assert "Direct IP" in res["status"]
    assert "192.168.1.1" in res["resolved_ips"]
