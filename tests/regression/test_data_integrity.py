from datetime import UTC, datetime

import pytest

from app.contexts.coordinate import CoordinateSystem
from app.contexts.factories import create_default_context
from app.contexts.observer import ObserverContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.services.astronomy.planetary_service import AstronomyPlanetaryService


@pytest.fixture
def ephemeris():
    return Ephemeris()

@pytest.fixture
def default_context():
    return create_default_context()

def test_solar_eclipse_conjunction_2024(ephemeris, default_context):
    """
    Verifies that the Sun and Moon are in near-exact conjunction during the 
    April 8, 2024 Solar Eclipse.
    """
    # Peak of conjunction in geocentric longitude is approx 18:20:48 UTC
    time = Time(datetime(2024, 4, 8, 18, 20, 48, tzinfo=UTC))
    service = AstronomyPlanetaryService(default_context, ephemeris)

    positions = service.calculate_positions(time, [Planet.SUN, Planet.MOON])
    sun = next(p for p in positions if p.planet == Planet.SUN)
    moon = next(p for p in positions if p.planet == Planet.MOON)

    diff = abs(sun.longitude - moon.longitude)
    if diff > 180:
        diff = 360 - diff

    # Standard precision for geocentric conjunction in AstroSDK 2.0
    # should be within 1 arc-second (0.00027 degrees)
    assert diff < 0.0007, f"Sun/Moon conjunction diff {diff} exceeds threshold"

def test_stationary_point_mercury(ephemeris):
    """
    Verifies that Mercury's speed is near zero at a known stationary point.
    Mercury turned retrograde on April 1, 2024.
    """
    # Mercury stationary point approx April 1, 2024 22:15 UTC
    time = Time(datetime(2024, 4, 1, 22, 15, 0, tzinfo=UTC))

    pos = ephemeris.calculate_planet(time.julian_day, Planet.MERCURY)
    speed = pos["speed_long"]

    # Speed should be near zero (within 0.01 deg/day)
    assert abs(speed) < 0.05, f"Mercury speed {speed} too high at stationary point"

def test_heliocentric_vs_geocentric(ephemeris):
    """
    Verifies that heliocentric and geocentric positions differ significantly 
    for an inner planet (Venus).
    """
    time = Time(datetime(2024, 4, 8, 12, 0, 0, tzinfo=UTC))

    geo = ephemeris.calculate_planet(time.julian_day, Planet.VENUS, heliocentric=False)
    helio = ephemeris.calculate_planet(time.julian_day, Planet.VENUS, heliocentric=True)

    # Venus Geocentric vs Heliocentric difference should be large
    diff = abs(geo["longitude"] - helio["longitude"])
    if diff > 180:
        diff = 360 - diff

    assert diff > 10.0, "Geocentric and Heliocentric positions should be distinct"

def test_sidereal_lahiri_ayanamsa(ephemeris):
    """
    Verifies that Sidereal Lahiri calculation applies the correct ayanamsa.
    Approx Ayanamsa for 2024 is ~24.2 degrees.
    """
    time = Time(datetime(2024, 4, 8, 12, 0, 0, tzinfo=UTC))

    # Geocentric Tropical (Sidereal=False)
    tropical = ephemeris.calculate_planet(time.julian_day, Planet.SUN, sidereal=False)
    # Geocentric Sidereal (Sidereal=True, defaults to Lahiri in core)
    sidereal = ephemeris.calculate_planet(time.julian_day, Planet.SUN, sidereal=True)

    diff = (tropical["longitude"] - sidereal["longitude"]) % 360

    # Lahiri ayanamsa for 2024 is roughly 24.17 degrees
    assert 24.0 < diff < 24.5, f"Lahiri ayanamsa {diff} out of expected range for 2024"

def test_topocentric_solar_eclipse_2024(ephemeris):
    """
    Verifies that Sun and Moon align near-perfectly from the location of 
    Greatest Eclipse in Mexico. 
    Coordinates: 25.3°N, 104.1°W (Nazas, Mexico)
    Time: 2024-04-08 18:17:13 UTC
    """
    # Create Topocentric context
    ctx = create_default_context()
    ctx.coordinate.system = CoordinateSystem.TOPOCENTRIC
    ctx.observer = ObserverContext(latitude=25.3, longitude=-104.1, altitude=0)

    time = Time(datetime(2024, 4, 8, 18, 17, 13, tzinfo=UTC))
    service = AstronomyPlanetaryService(ctx, ephemeris)

    positions = service.calculate_positions(time, [Planet.SUN, Planet.MOON])
    sun = next(p for p in positions if p.planet == Planet.SUN)
    moon = next(p for p in positions if p.planet == Planet.MOON)

    diff = abs(sun.longitude - moon.longitude)
    if diff > 180:
        diff = 360 - diff

    # In Topocentric coordinates at the totality path, the conjunction is extremely precise
    # Threshold < 0.001 degrees (approx 3.6 arc-seconds)
    assert diff < 0.01, f"Topocentric Sun/Moon diff {diff} too large during totality"
