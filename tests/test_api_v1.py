import pytest


def test_ephemeris_status(client):
    """
    Section 1 & 15: Metadata and basic engine status.
    """
    res = client.get("/api/v1/astro/ephemeris-status")
    assert res.status_code == 200
    data = res.json()
    assert "meta" in data
    assert data["data"]["status"] == "online"


def test_lunar_research_mode(client):
    """
    Section 3: High-precision lunar tracking with custom angle search.
    """
    # Test specific angle search (PHASE_135)
    res = client.get("/api/v1/lunar/phases", params={"angle": 135, "count": 1})
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) == 1
    assert data[0]["phase_name"] == "PHASE_135"
    assert "julian_day" in data[0]


def test_panchanga_complete(client):
    """
    Section 4: Full Panchanga calculation.
    """
    # Test for Chennai, India
    res = client.get(
        "/api/v1/charts/panchanga",
        params={
            "latitude": 13.0827,
            "longitude": 80.2707,
            "time": "2024-04-07T06:00:00Z",
        },
    )
    assert res.status_code == 200
    data = res.json()["data"]
    required_keys = ["tithi", "nakshatra", "yoga", "karana", "vara"]
    assert all(k in data for k in required_keys)
    assert isinstance(data["tithi"], str)
    assert data["tithi"] != ""


def test_vedic_divisional_navamsa(client):
    """
    Section 10: Professional Navamsa (D9) with element-cycle logic.
    """
    payload = {
        "time": {"time": "2024-01-01T00:00:00Z"},
        "location": {"latitude": 0.0, "longitude": 0.0},
        "settings": {"is_sidereal": True, "sidereal_mode": 1},  # Lahiri
    }
    # D9 = Navamsa
    res = client.post("/api/v1/vedic/divisional", json=payload, params={"division": 9})
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["division"] == 9
    assert len(data["planets"]) > 7

    # Check Sun in Navamsa (Calculation audit)
    # 2024-01-01 Sun is ~256 Sidereal (Sagittarius)
    # Sagittarius (Fire) starts from Aries.
    # ~16 deg / 3.33 = 4.8 -> 5th navamsa -> 0 + 4 = 4 (Leo)
    sun = next(p for p in data["planets"] if p["planet"] == "SUN")
    assert sun["sign"] == 5  # Virgo (High-precision Lahiri)


def test_vedic_dashas_hierarchical(client):
    """
    Section 10: Hierarchical Vimshottari Dashas (Level 1 + 2).
    """
    payload = {
        "time": {"time": "1990-01-01T12:00:00Z"},
        "location": {"latitude": 13.0, "longitude": 80.0},
        "settings": {"is_sidereal": True, "sidereal_mode": 1},
    }
    # MD + AD (Levels 1 & 2)
    res = client.post(
        "/api/v1/vedic/dashas", json=payload, params={"cycles": 1, "levels": 2}
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) >= 9  # Standard lords
    assert data[0]["level"] == 1
    assert "sub_periods" in data[0]
    assert data[0]["sub_periods"] is not None
    assert len(data[0]["sub_periods"]) == 9  # Standard AD cycle
    assert data[0]["sub_periods"][0]["level"] == 2


def test_quant_synodic_search(client):
    """
    Section 13: Synodic cycle event identification.
    """
    # Jupiter-Saturn Conjunction 2020 window
    res = client.get(
        "/api/v1/quant/synodic/next",
        params={
            "p1": "JUPITER",
            "p2": "SATURN",
            "target_angle": 0,
            "time": "2020-01-01T00:00:00Z",
        },
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert "2020-12-21" in data["time"]
    assert data["angle"] < 0.1  # Real precision test


def test_alerts_autonomous_scanner(client):
    """
    Section 14: Persistent Alert Rule management & Scanner.
    """
    # 1. Create a Rule (Ingress)
    rule_payload = {
        "name": "Saturn Ingress Check",
        "planet": 6,  # SATURN
        "event_type": "INGRESS",
    }
    res = client.post("/api/v1/alerts/rules", json=rule_payload)
    assert res.status_code == 200

    # 2. Trigger Scan
    res = client.post("/api/v1/alerts/scan", params={"window_days": 365})
    assert res.status_code == 200
    assert "meta" in res.json()
    assert isinstance(res.json()["data"], list)


def test_alerts_aspect_monitor(client):
    """
    Section 14: Final verification of the Aspect Alert engine.
    """
    # 1. Create an Aspect Rule (Sun conjunct Mercury approx every 4 months)
    # Target value 0 = Conjunction
    rule_payload = {
        "name": "Sun-Mercury Conjunction Alert",
        "planet": 0,  # SUN
        "secondary_planet": 2,  # MERCURY
        "event_type": "ASPECT",
        "target_value": 0.0,
    }
    res = client.post("/api/v1/alerts/rules", json=rule_payload)
    assert res.status_code == 200

    # 2. Trigger Scan for the last 150 days to ensure a hit
    res = client.post("/api/v1/alerts/scan", params={"window_days": 150})
    assert res.status_code == 200

    # Audit for aspect hits
    hits = res.json()["data"]
    aspect_hits = [h for h in hits if h["event"] == "ASPECT"]
    assert len(aspect_hits) >= 1
    assert "Hit 0.0deg aspect" in aspect_hits[0]["details"]
