from datetime import UTC, datetime

from app.core.constants import Planet, SiderealMode
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.services.crossing_service import CrossingService
from app.services.events_service import EventsService

def test_jupiter_ingress_2024():
    """
    Verify Jupiter ingress into Taurus (Sidereal Lahiri).
    Approx date: 2024-05-01
    """
    eph = Ephemeris()
    crossing_service = CrossingService(eph)
    events_service = EventsService(eph, crossing_service)

    start = Time.from_string("2024-04-25 00:00:00")
    
    events = events_service.get_sign_ingresses(start, Planet.JUPITER, count=1, sidereal_mode=SiderealMode.LAHIRI)

    # Sign 0 = Aries, 1 = Taurus
    assert len(events) > 0
    ingress = events[0]
    assert ingress.to_sign == "TAURUS"

    t_ingress = ingress.time
    assert t_ingress.month == 5
    assert t_ingress.day == 1

def test_mercury_station_2024():
    """
    Verify Mercury station direct in early 2024.
    Approx: Jan 2, 2024.
    """
    eph = Ephemeris()
    crossing_service = CrossingService(eph)
    events_service = EventsService(eph, crossing_service)

    start = Time.from_string("2023-12-30 00:00:00")

    events = events_service.get_retrograde_stations(start, Planet.MERCURY, count=2)

    # Station direct: speed_after > 0 usually
    station = next((e for e in events if e.station_type == "DIRECT"), None)
    if not station:
        station = events[0]

    t_station = station.time
    assert t_station.month == 1
    assert t_station.day == 2

def test_solar_return_2024():
    """
    Verify Solar Return calculation.
    """
    eph = Ephemeris()
    crossing_service = CrossingService(eph)

    # Sun at 0 Aries (Tropical for simple verification check or Sidereal 0 Aries)
    # Let's use Sidereal Lahiri 0 Aries (Vernal Equinox - Ayanamsa)
    target_long = 0.0 # 0 Aries
    start_time = Time.from_string("2024-04-10 00:00:00")

    t_return = crossing_service.find_planetary_return(Planet.SUN, target_long, start_time)

    assert t_return is not None
    dt = t_return.dt
    # Sidereal Sun enters Aries approx April 13-14
    assert dt.month == 4
    assert 13 <= dt.day <= 15

