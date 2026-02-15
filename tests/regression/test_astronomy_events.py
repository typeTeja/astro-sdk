import pytest
from astrosdk.core.time import Time
from astrosdk.core.constants import Planet, SiderealMode
from astrosdk.engine.event_engine import EventEngine
from astrosdk.engine.cycle_engine import CycleEngine
from datetime import datetime, timezone

def test_jupiter_ingress_2024():
    """
    Verify Jupiter ingress into Taurus (Sidereal Lahiri).
    Approx date: 2024-05-01
    """
    engine = EventEngine()
    start = Time.from_string("2024-04-25 00:00:00")
    end = Time.from_string("2024-05-05 00:00:00")
    
    events = engine._event_service.scan_ingresses(Planet.JUPITER, start, end)
    
    # Sign 0 = Aries, 1 = Taurus
    ingress = next((e for e in events if e.data.get("sign_to") == "1"), None)
    assert ingress is not None
    
    # Check JD matches approx expected time
    # May 1, 2024 07:30 UTC approx (Vedic calc check)
    t_ingress = datetime.fromtimestamp((ingress.julian_day - 2440587.5) * 86400.0, tz=timezone.utc)
    assert t_ingress.month == 5
    assert t_ingress.day == 1

def test_mercury_station_2024():
    """
    Verify Mercury station direct in early 2024.
    Approx: Jan 2, 2024.
    """
    engine = EventEngine()
    start = Time.from_string("2023-12-30 00:00:00")
    end = Time.from_string("2024-01-05 00:00:00")
    
    events = engine._event_service.scan_stations(Planet.MERCURY, start, end)
    
    # Station direct: speed_before < 0, speed_after > 0
    station = next((e for e in events if float(e.data["speed_before"]) < 0), None)
    assert station is not None
    
    t_station = datetime.fromtimestamp((station.julian_day - 2440587.5) * 86400.0, tz=timezone.utc)
    assert t_station.month == 1
    assert t_station.day == 2

def test_solar_return_2024():
    """
    Verify Solar Return calculation.
    """
    engine = CycleEngine()
    # Sun at 0 Aries (Tropical for simple verification check or Sidereal 0 Aries)
    # Let's use Sidereal Lahiri 0 Aries (Vernal Equinox - Ayanamsa)
    target_long = 0.0 # 0 Aries
    start_time = Time.from_string("2024-04-10 00:00:00")
    
    # We need to use internal cycle service for now or public Engine method if implemented
    cycle_event = engine._cycle_service.compute_return(Planet.SUN, target_long, start_time)
    
    assert cycle_event is not None
    t_return = datetime.fromtimestamp((cycle_event.exact_time - 2440587.5) * 86400.0, tz=timezone.utc)
    # Sidereal Sun enters Aries approx April 13-14
    assert t_return.month == 4
    assert 13 <= t_return.day <= 15
