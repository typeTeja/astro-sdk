import pytest
from datetime import datetime, timezone, timedelta
from astrosdk.core.time import Time
from astrosdk.core.ephemeris import Ephemeris
from astrosdk.core.constants import Planet, SiderealMode
from astrosdk.services.crossing_service import CrossingService
from astrosdk.services.natal_service import NatalService

@pytest.fixture
def ephemeris():
    return Ephemeris()

@pytest.fixture
def crossing_service(ephemeris):
    return CrossingService(ephemeris)

@pytest.fixture
def natal_service(ephemeris):
    return NatalService(ephemeris)

class TestCrossingService:
    def test_solar_return(self, crossing_service, natal_service):
        """Test solar return calculation."""
        # Use a mid-year date (May 20) to avoid year-wrap boundary issues in testing
        birth_time = Time(datetime(2000, 5, 20, 12, 0, tzinfo=timezone.utc))
        natal_pos = natal_service.calculate_positions(birth_time)
        sun_long = next(p.longitude for p in natal_pos if p.planet == Planet.SUN)
        
        # Find return in 2001
        return_time = crossing_service.find_solar_return(sun_long, 2001)
        
        # Verify Sun is at natal longitude at return time
        return_pos = natal_service.calculate_positions(return_time)
        return_sun_long = next(p.longitude for p in return_pos if p.planet == Planet.SUN)
        
        # Tolerance: 0.01 degree
        assert abs(return_sun_long - sun_long) < 0.01
        assert return_time.dt.year == 2001

    def test_lunar_return(self, crossing_service, natal_service):
        """Test lunar return calculation (monthly cycle)."""
        birth_time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        natal_pos = natal_service.calculate_positions(birth_time)
        moon_long = next(p.longitude for p in natal_pos if p.planet == Planet.MOON)
        
        # Find next return (after ~27.3 days)
        # We start searching from 20 days after birth to avoid catching the birth moment
        search_start = Time(birth_time.dt + timedelta(days=20))
        return_time = crossing_service.find_lunar_return(moon_long, search_start)
        
        return_pos = natal_service.calculate_positions(return_time)
        return_moon_long = next(p.longitude for p in return_pos if p.planet == Planet.MOON)
        
        assert abs(return_moon_long - moon_long) < 0.01
        # Should be roughly 27-28 days later
        diff_days = (return_time.dt - birth_time.dt).total_seconds() / 86400
        assert 26 < diff_days < 29

    def test_ingress_mars(self, crossing_service, natal_service):
        """Test planetary ingress detection."""
        # Mars at ~316.5 deg on Jan 1 2000
        start_time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        
        # Find next ingress
        ingress_time, sign_num = crossing_service.find_next_ingress(Planet.MARS, start_time)
        
        # Verify at ingress time Mars is at 0/30/60... degree
        ingress_pos = natal_service.calculate_positions(ingress_time)
        mars_long = next(p.longitude for p in ingress_pos if p.planet == Planet.MARS)
        
        assert abs(mars_long % 30) < 0.01
        # Sign number should match
        expected_sign = int((mars_long / 30.0) % 12) + 1
        assert sign_num == expected_sign

    def test_heliocentric_return(self, crossing_service, ephemeris):
        """Test heliocentric return calculation."""
        # Mars heliocentric return
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        
        pos = ephemeris.calculate_planet(time.julian_day, Planet.MARS, sidereal=True, heliocentric=True)
        target_lon = pos["longitude"]
        
        # Find next return (Mars orbital period ~1.88 years)
        search_start = Time(time.dt + timedelta(days=600))
        return_time = crossing_service.find_planetary_return(
            Planet.MARS, target_lon, search_start, heliocentric=True, max_search_years=2.0
        )
        
        return_pos = ephemeris.calculate_planet(return_time.julian_day, Planet.MARS, sidereal=True, heliocentric=True)
        assert abs(return_pos["longitude"] - target_lon) < 0.01
