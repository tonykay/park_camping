import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_parks():
    resp = client.get("/parks")
    assert resp.status_code == 200
    parks = resp.json()
    assert isinstance(parks, list)
    assert len(parks) == 5

def test_get_park():
    parks = client.get("/parks").json()
    park_id = parks[0]["id"]
    resp = client.get(f"/parks/{park_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == park_id

def test_list_campgrounds():
    parks = client.get("/parks").json()
    park_id = parks[0]["id"]
    resp = client.get(f"/parks/{park_id}/campgrounds")
    assert resp.status_code == 200
    campgrounds = resp.json()
    assert isinstance(campgrounds, list)
    assert len(campgrounds) >= 2

def test_get_campground():
    parks = client.get("/parks").json()
    park_id = parks[0]["id"]
    campgrounds = client.get(f"/parks/{park_id}/campgrounds").json()
    cg_id = campgrounds[0]["id"]
    resp = client.get(f"/campgrounds/{cg_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == cg_id

def test_list_campsites():
    parks = client.get("/parks").json()
    park_id = parks[0]["id"]
    campgrounds = client.get(f"/parks/{park_id}/campgrounds").json()
    cg_id = campgrounds[0]["id"]
    resp = client.get(f"/campgrounds/{cg_id}/sites")
    assert resp.status_code == 200
    sites = resp.json()
    assert isinstance(sites, list)
    assert len(sites) > 0

def test_get_availability():
    parks = client.get("/parks").json()
    park_id = parks[0]["id"]
    campgrounds = client.get(f"/parks/{park_id}/campgrounds").json()
    cg_id = campgrounds[0]["id"]
    resp = client.get(f"/campgrounds/{cg_id}/availability", params={"start_date": "2025-07-01", "nights": 2})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)

def test_get_costs():
    parks = client.get("/parks").json()
    park_id = parks[0]["id"]
    campgrounds = client.get(f"/parks/{park_id}/campgrounds").json()
    cg_id = campgrounds[0]["id"]
    resp = client.get(f"/campgrounds/{cg_id}/costs")
    assert resp.status_code == 200
    costs = resp.json()
    assert isinstance(costs, dict)
    assert all(isinstance(v, float) or isinstance(v, int) for v in costs.values())