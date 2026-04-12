from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_root_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json()["version"] == "2.0.0"

def test_v2_astronomy_planet_position():
    # Generic Test
    response = client.get("/api/v2/astronomy/planet-position?planet=SUN&time=2024-04-08T18:00:00Z")
    assert response.status_code == 200
    assert "position" in response.json()
    assert response.json()["planet"] == "SUN"

def test_v2_historical_gold_eclipse():
    """
    Historical Gold: 2024 Total Solar Eclipse in Torreón, Mexico.
    Sun and Moon should be in exact conjunction.
    """
    time = "2024-04-08T18:17:15Z"
    lat = 25.5439
    lon = -103.4190

    # Get Sun
    sun_res = client.get(f"/api/v2/astronomy/planet-position?planet=SUN&time={time}&coordinate_system=topocentric&latitude={lat}&longitude={lon}")
    # Get Moon
    moon_res = client.get(f"/api/v2/astronomy/planet-position?planet=MOON&time={time}&coordinate_system=topocentric&latitude={lat}&longitude={lon}")

    assert sun_res.status_code == 200
    assert moon_res.status_code == 200

    sun_lon = sun_res.json()["position"]["longitude"]
    moon_lon = moon_res.json()["position"]["longitude"]

    # Precision should be high for topocentric calculation
    assert abs(sun_lon - moon_lon) < 0.05

def test_v2_historical_gold_einstein():
    """
    Historical Gold: Albert Einstein's Natal Chart.
    Verifying House Cusps (Placidus).
    """
    payload = {
        "time": {"time": "1879-03-14T10:50:00Z"},
        "location": {"latitude": 48.3984, "longitude": 9.9915},
        "settings": {"house_system": "P", "is_sidereal": False}
    }
    response = client.post("/api/v2/charts/natal", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]

    # Expected Ascendant around 101.62° (11°37' Cancer)
    # Expected MC around 342.95° (12°57' Pisces)
    assert abs(data["ascendant"] - 101.62) < 0.2
    assert abs(data["mc"] - 342.95) < 0.2

def test_v2_charts_transits():
    response = client.get("/api/v2/charts/transits?latitude=40.7128&longitude=-74.0060&time=2024-04-08T18:00:00Z")
    assert response.status_code == 200
    assert "planets" in response.json()["data"]

def test_v2_aspects_calculate():
    response = client.get("/api/v2/aspects/calculate?time=2024-04-08T18:00:00Z&planets=SUN&planets=MOON")
    assert response.status_code == 200
    assert "aspects" in response.json()["data"]

def test_v2_vedic_panchang():
    response = client.get("/api/v2/vedic/panchang?latitude=18.5204&longitude=73.8567&time=2024-04-08T06:00:00Z")
    assert response.status_code == 200
    assert "tithi" in response.json()["data"]

def test_v2_progressions_secondary():
    response = client.get("/api/v2/progressions/secondary?birth_time=1980-01-01T00:00:00Z&target_date=2024-01-01T00:00:00Z")
    assert response.status_code == 200
    assert "planets" in response.json()["data"]

def test_v2_financial_time_windows():
    response = client.get("/api/v2/financial/time-windows?preset=big_shifts&start_time=2024-04-08T18:00:00Z")
    assert response.status_code == 200
    assert "windows" in response.json()["data"]

def test_v2_quant_synodic_phase():
    response = client.get("/api/v2/quant/synodic/phase?p1=SUN&p2=MOON&time=2024-04-08T18:00:00Z")
    assert response.status_code == 200
    assert "phase" in response.json()["data"]

def test_v2_signals_intensity():
    response = client.get("/api/v2/signals/astro-intensity?max_days=7&start_time=2024-04-08T18:00:00Z")
    assert response.status_code == 200
    assert "intensities" in response.json()["data"]

def test_v2_heliacal_rising():
    # Requires location
    response = client.get("/api/v2/heliacal/rising?planet=VENUS&latitude=40.7128&longitude=-74.0060&time=2024-04-08T18:00:00Z")
    assert response.status_code == 200
    assert "time" in response.json()["data"]

def test_v2_vedic_divisional():
    payload = {
        "time": {"time": "2024-04-08T18:00:00Z"},
        "location": {"latitude": 25.5439, "longitude": -103.4190}
    }
    # D9 Navamsa
    response = client.post("/api/v2/vedic/classic/divisional?division=9", json=payload)
    assert response.status_code == 200
    assert "planets" in response.json()["data"]

def test_v2_vedic_dashas():
    payload = {
        "time": {"time": "2024-04-08T18:00:00Z"},
        "location": {"latitude": 25.5439, "longitude": -103.4190}
    }
    response = client.post("/api/v2/vedic/classic/dashas", json=payload)
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)
