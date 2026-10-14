from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_pasted_text_scan_api():
    payload = {
        "text": "Hurry! Only 2 items left in stock - Order within 03m 12s!",
        "language": "en"
    }
    response = client.post("/api/v1/scans/text", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] > 0
    assert len(data["findings"]) > 0

def test_compliance_guidelines_api():
    response = client.get("/api/v1/compliance/guidelines")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 13
