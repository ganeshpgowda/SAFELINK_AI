"""Integration tests for SafeLink AI FastAPI REST API endpoints.
"""

from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "SafeLink AI" in data["title"]
    assert data["model_loaded"] is True


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


def test_analyze_endpoint_success():
    payload = {"url": "https://en.wikipedia.org/wiki/Main_Page"}
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == payload["url"]
    assert "risk" in data
    assert "score" in data["risk"]
    assert "factors" in data
    assert "recommendations" in data
    assert "anatomy" in data
    assert "privacy_notice" in data


def test_analyze_endpoint_empty_url():
    response = client.post("/analyze", json={"url": "   "})
    assert response.status_code == 400


def test_batch_analyze_endpoint():
    payload = {
        "urls": [
            "https://www.google.com",
            "http://192.168.1.100/login",
            "https://bit.ly/claim-bonus-2026"
        ]
    }
    response = client.post("/batch-analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert data["summary"]["total_analyzed"] == 3
    assert len(data["results"]) == 3


def test_features_endpoint():
    response = client.get("/features")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 28
    names = [f["name"] for f in data]
    assert "url_length" in names
    assert "is_ip" in names


def test_sample_urls_endpoint():
    response = client.get("/sample-urls")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5
    assert "url" in data[0]


def test_stats_endpoint():
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["model_type"] == "RandomForestClassifier"
    assert "evaluation_metrics" in data
    assert "top_predictive_features" in data

