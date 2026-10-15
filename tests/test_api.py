from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
VALID = {"age": 0.02, "sex": -0.044, "bmi": 0.06, "bp": -0.03, "s1": -0.02,
         "s2": 0.03, "s3": -0.02, "s4": 0.02, "s5": 0.02, "s6": -0.001}

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"

def test_predict_ok():
    r = client.post("/predict", json=VALID)
    assert r.status_code == 200 and isinstance(r.json()["prediction"], float)

def test_missing_field_422():
    bad = {k: v for k, v in VALID.items() if k != "s6"}
    assert client.post("/predict", json=bad).status_code == 422

def test_wrong_type_422():
    assert client.post("/predict", json={**VALID, "age": "abc"}).status_code == 422