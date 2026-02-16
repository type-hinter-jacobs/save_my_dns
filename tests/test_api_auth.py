from fastapi.testclient import TestClient
from src.api.app import app


client = TestClient(app)

def test_post_blocked_domains_requires_api_key():
    resp = client.post("/blocked-domains", json={"domain": "porn.com"}, headers=None)
    assert resp.status_code == 401

def test_post_blocked_domains_rejects_invalid_api_key():
    resp = client.post("/blocked-domains", json={"domain": "porn.com"}, headers={"X-API-Key": "wrong-value"})
    assert resp.status_code == 401

def test_post_blocked_domains_accepts_correct_api_key(monkeypatch, override_get_repo):
    test_key = "123456789"
    monkeypatch.setenv("SAVE_MY_DNS_ADMIN_KEY", test_key)
    resp = client.post("/blocked-domains", json={"domain": "porn.com"}, headers={"X-API-Key": test_key})
    assert resp.status_code == 201

def test_patch_blocked_domains_accepts_correct_api_key(monkeypatch, override_get_repo):
    test_key = "123456789"
    monkeypatch.setenv("SAVE_MY_DNS_ADMIN_KEY", test_key)
    resp = client.post("/blocked-domains", json={"domain": "porn.com"}, headers={"X-API-Key": test_key})
    assert resp.status_code == 201
    resp = client.patch("/blocked-domains/porn.com", json={"enabled": False}, headers={"X-API-Key": test_key})
    assert resp.status_code == 200
    assert resp.json()["enabled"] is False
    resp = client.get("/blocked-domains")
    found = False
    for item in resp.json():
        if item["domain"] == "porn.com":
            found = True
            assert item["enabled"] is False
    assert found is True

def test_delete_blocked_domains_accepts_correct_api_key(monkeypatch, override_get_repo):
    test_key = "123456789"
    monkeypatch.setenv("SAVE_MY_DNS_ADMIN_KEY", test_key)
    resp = client.post("/blocked-domains", json={"domain": "porn.com"}, headers={"X-API-Key": test_key})
    assert resp.status_code == 201
    resp = client.delete("/blocked-domains/porn.com", headers={"X-API-Key": test_key})
    assert resp.status_code == 204
    resp = client.get("/blocked-domains")
    found = False
    for item in resp.json():
        if item["domain"] == "porn.com":
            found = True
    assert found is False

