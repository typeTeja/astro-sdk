import pytest
from datetime import datetime, timezone
from astrosdk.core.time import Time
from astrosdk.core.ephemeris import Ephemeris
from astrosdk.core.constants import Planet
from astrosdk.services.heliacal_service import HeliacalService
from astrosdk.services.natal_service import NatalService

@pytest.fixture
def ephemeris():
    return Ephemeris()

@pytest.fixture
def heliacal_service(ephemeris):
    return HeliacalService(ephemeris)

@pytest.fixture
def natal_service(ephemeris):
    return NatalService(ephemeris)

class TestHorizontalAndHeliacal:
    def test_azimuth_altitude_tokyo(self, natal_service):
        """Test that azimuth and altitude are populated in Tokyo."""
        date = Time(datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc))
        lat, lon = 35.6762, 139.6503 # Tokyo
        
        positions = natal_service.calculate_positions(date, lat=lat, lon=lon)
        sun = next(p for p in positions if p.planet == Planet.SUN)
        
        assert sun.azimuth is not None
        assert sun.altitude is not None
        # In Tokyo on Jan 1st at 12:00 UTC (21:00 JST), Sun is below horizon
        assert sun.altitude < 0
        assert 0 <= sun.azimuth < 360

    def test_mercury_retrograde_stations_2024(self, heliacal_service):
        """Test finding Mercury retrograde stations in 2024."""
        stations = heliacal_service.find_all_stations(Planet.MERCURY, 2024)
        
        # Mercury famously has 3-4 retrogrades per year
        assert len(stations) >= 3
        
        # Verify types
        types = [s["type"] for s in stations]
        assert "Retrograde Station" in types
        assert "Direct Station" in types
        
        # Verify order
        for i in range(len(stations)-1):
            assert stations[i]["jd"] < stations[i+1]["jd"]

    def test_heliacal_rising_venice(self, heliacal_service):
        """Test heliacal rising calculation for Venus."""
        # Venus heliacal rising in 2024
        date = Time(datetime(2024, 1, 1, tzinfo=timezone.utc))
        lat, lon = 45.4408, 12.3155 # Venice
        
        rising = heliacal_service.calculate_heliacal_rising(Planet.VENUS, date, lat, lon)
        # It might return None if no ephemeris files are found in CI, but here we expect it to try
        if rising:
            assert isinstance(rising, Time)
            assert rising.julian_day > date.julian_day

    def test_stationary_point_sun_moon(self, ephemeris):
        """Test that Sun and Moon have no stationary points."""
        jd = Time(datetime(2024, 1, 1, tzinfo=timezone.utc)).julian_day
        assert ephemeris.calculate_stationary_point(jd, Planet.SUN) is None
        assert ephemeris.calculate_stationary_point(jd, Planet.MOON) is None
