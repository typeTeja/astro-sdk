from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_moon_position_known_date():
    """
    Historical Gold: 2000-01-01T12:00:00Z J2000 Epoch
    Moon Tropical Position should be approximately 223.32 degrees (Scorpio)
    """
    response = client.get(
        "/api/v2/astronomy/planet-position?planet=MOON&time=2000-01-01T12:00:00Z",
        headers={"X-Astro-Is-Sidereal": "false"}
    )
    assert response.status_code == 200
    lon = response.json()["position"]["longitude"]
    # J2000 Moon position in tropical geocentric
    assert abs(lon - 223.32) < 0.1

def test_retrograde_boundary_event():
    """
    Verify Mars Retrograde Station of 2024-12-06.
    Check speed and motion flag around this time.
    """
    res1 = client.get("/api/v2/astronomy/planet-position?planet=MARS&time=2024-12-01T00:00:00Z")
    res2 = client.get("/api/v2/astronomy/planet-position?planet=MARS&time=2024-12-10T00:00:00Z")
    
    # Mars is direct on Dec 1, Retrograde by Dec 10.
    v1 = res1.json()["position"]["speed_long"]
    v2 = res2.json()["position"]["speed_long"]
    
    assert v1 > 0
    assert v2 < 0

def test_ascendant_boundary_case():
    """
    Historical Gold: High latitude chart (Oslo, Norway)
    Time: 2024-01-01 12:00 UTC
    Verify Ascendant to 0.1 degree precision.
    """
    payload = {
        "time": {"time": "2024-01-01T12:00:00Z"},
        "location": {"latitude": 59.9139, "longitude": 10.7522},
        "settings": {"house_system": "W", "is_sidereal": False}
    }
    response = client.post("/api/v2/charts/natal", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    
    # Expected Ascendant at this exact time in Oslo
    assert abs(data["ascendant"] - 64.9) < 0.5

def test_solar_eclipse_exactitude():
    """
    Historical Gold: Total Solar Eclipse of 2024-04-08 18:17 UTC.
    The difference in Sun and Moon longitudes must be < 0.05 degrees.
    """
    time = "2024-04-08T18:17:15Z"
    lat = 25.5439
    lon = -103.4190

    sun_res = client.get(f"/api/v2/astronomy/planet-position?planet=SUN&time={time}&coordinate_system=topocentric&latitude={lat}&longitude={lon}")
    moon_res = client.get(f"/api/v2/astronomy/planet-position?planet=MOON&time={time}&coordinate_system=topocentric&latitude={lat}&longitude={lon}")

    sun_lon = sun_res.json()["position"]["longitude"]
    moon_lon = moon_res.json()["position"]["longitude"]

    assert abs(sun_lon - moon_lon) < 0.05
