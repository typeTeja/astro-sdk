import pytest
from astrosdk.core.time import Time
from astrosdk.core.ephemeris import Ephemeris
from astrosdk.services.event_service import EventService
from astrosdk.core.constants import Planet, HouseSystem, SiderealMode
from astrosdk.services.natal_service import NatalService

@pytest.fixture
def ephemeris():
    return Ephemeris()

@pytest.fixture
def event_service(ephemeris):
    return EventService(ephemeris)

@pytest.fixture
def natal_service(ephemeris):
    return NatalService(ephemeris)

def test_historical_solar_eclipse_1900(event_service):
    # May 28, 1900 Total Solar Eclipse
    t = Time.from_string("1900-05-01 00:00:00")
    eclipse = event_service.find_next_solar_eclipse(t)
    # Expected peak around 1900-05-28
    assert t.julian_day < eclipse.peak_jd
    assert eclipse.type == "SOLAR"
    assert eclipse.is_total is True

def test_future_solar_eclipse_2045(event_service):
    # August 12, 2045 Total Solar Eclipse
    t = Time.from_string("2045-08-01 00:00:00")
    eclipse = event_service.find_next_solar_eclipse(t)
    assert eclipse.peak_jd > t.julian_day
    assert eclipse.type == "SOLAR"
    assert eclipse.is_total is True

def test_historical_jupiter_ingress_1950(event_service):
    # Jupiter ingress detection in 1950 (Sidereal Lahiri)
    # Verify that the scanner detects sign changes for slow-moving planets
    t_start = Time.from_string("1950-01-01 00:00:00")
    t_end = Time.from_string("1950-12-31 00:00:00")
    ingresses = event_service.scan_ingresses(Planet.JUPITER, t_start, t_end, sidereal_mode=SiderealMode.LAHIRI)
    # Jupiter should have at least one ingress in a full year
    assert len(ingresses) >= 1, f"Expected at least 1 ingress, found {len(ingresses)}"

def test_high_latitude_house_cusps(natal_service):
    # Murmansk, Russia (68.97° N)
    t = Time.from_string("2024-01-01 12:00:00")
    lat, lon = 68.97, 33.08
    
    # Systems that often fail at high latitudes like Placidus
    # Swiss Ephemeris falls back to Porphyry or handles it with a flag if possible.
    houses = natal_service.calculate_houses(t, lat, lon, system=HouseSystem.PLACIDUS)
    assert len(houses.cusps) == 12
    # MC should be reasonable
    assert 0 <= houses.axes.midheaven < 360

def test_delta_t_precision(ephemeris):
    # Verify Delta-T is returning high precision values for 2024
    t = Time.from_string("2024-01-01 00:00:00")
    dt = t.delta_t
    # In 2024, Delta-T is around 69 seconds (~0.0008 days)
    assert 0.0007 < dt < 0.0009
