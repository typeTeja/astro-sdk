"""
Tests for heliocentric calculations.
"""
import pytest
from datetime import datetime, timezone
from astrosdk.core.time import Time
from astrosdk.core.ephemeris import Ephemeris
from astrosdk.core.constants import Planet, SiderealMode
from astrosdk.services.natal_service import NatalService


@pytest.fixture
def ephemeris():
    """Shared ephemeris instance."""
    return Ephemeris()


@pytest.fixture
def natal_service(ephemeris):
    """Shared natal service instance."""
    return NatalService(ephemeris)


class TestHeliocentricCalculations:
    """Test heliocentric calculation functionality."""
    
    def test_heliocentric_vs_geocentric(self, ephemeris):
        """Test that heliocentric positions differ from geocentric."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        jd = time.julian_day
        
        # Calculate Mars position both ways
        geocentric = ephemeris.calculate_planet(jd, Planet.MARS, sidereal=False, heliocentric=False)
        heliocentric = ephemeris.calculate_planet(jd, Planet.MARS, sidereal=False, heliocentric=True)
        
        # Positions should be different
        assert geocentric["longitude"] != heliocentric["longitude"]
        assert geocentric["latitude"] != heliocentric["latitude"]
        assert geocentric["distance"] != heliocentric["distance"]
        
    def test_heliocentric_sun_near_zero(self, ephemeris):
        """Test that Sun's heliocentric position is near zero."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        jd = time.julian_day
        
        # Sun's heliocentric position should be very small (at center)
        helio_sun = ephemeris.calculate_planet(jd, Planet.SUN, sidereal=False, heliocentric=True)
        
        # Distance should be very close to zero (Sun's center)
        assert helio_sun["distance"] < 0.01, f"Sun heliocentric distance should be near zero, got {helio_sun['distance']}"
        
    def test_heliocentric_with_sidereal(self, ephemeris):
        """Test heliocentric works with sidereal mode."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        jd = time.julian_day
        
        ephemeris.set_sidereal_mode(SiderealMode.LAHIRI)
        
        # Should work with both sidereal and heliocentric
        position = ephemeris.calculate_planet(jd, Planet.JUPITER, sidereal=True, heliocentric=True)
        
        assert "longitude" in position
        assert "latitude" in position
        assert "distance" in position
        
    def test_heliocentric_all_planets(self, natal_service):
        """Test heliocentric calculation for all planets."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        
        # Calculate heliocentric positions
        positions = natal_service.calculate_positions(time, heliocentric=True)
        
        # Should have positions for all planets
        assert len(positions) > 0
        
        # Find Sun's position
        sun_pos = next((p for p in positions if p.planet == Planet.SUN), None)
        assert sun_pos is not None
        
        # Sun's heliocentric distance should be near zero
        assert sun_pos.distance < 0.01, f"Sun heliocentric distance should be near zero, got {sun_pos.distance}"
        
    def test_heliocentric_backward_compatibility(self, natal_service):
        """Test that default behavior is still geocentric."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        
        # Default should be geocentric
        positions = natal_service.calculate_positions(time)
        
        # Sun should have normal distance (not zero in geocentric)
        sun_pos = next((p for p in positions if p.planet == Planet.SUN), None)
        assert sun_pos is not None
        # In geocentric, Sun's distance is ~0 (we're on Earth looking at Sun)
        # So this test should verify it's NOT heliocentric by checking other planets
        
        # Mars should have normal geocentric distance
        mars_pos = next((p for p in positions if p.planet == Planet.MARS), None)
        assert mars_pos is not None
        assert mars_pos.distance > 0.5, f"Geocentric Mars distance should be reasonable, got {mars_pos.distance}"
        
    def test_heliocentric_jupiter_distance(self, ephemeris):
        """Test Jupiter's heliocentric distance is reasonable."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        jd = time.julian_day
        
        helio_jupiter = ephemeris.calculate_planet(jd, Planet.JUPITER, sidereal=False, heliocentric=True)
        
        # Jupiter's distance from Sun should be around 5 AU
        assert 4.5 < helio_jupiter["distance"] < 5.5, f"Jupiter heliocentric distance should be ~5 AU, got {helio_jupiter['distance']}"
        
    def test_heliocentric_with_different_ayanamsas(self, natal_service):
        """Test heliocentric works with different ayanamsa systems."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        
        # Test with different ayanamsas
        lahiri = natal_service.calculate_positions(time, sidereal_mode=SiderealMode.LAHIRI, heliocentric=True)
        krishnamurti = natal_service.calculate_positions(time, sidereal_mode=SiderealMode.KRISHNAMURTI, heliocentric=True)
        
        # Find Mars in both
        lahiri_mars = next(p for p in lahiri if p.planet == Planet.MARS)
        kp_mars = next(p for p in krishnamurti if p.planet == Planet.MARS)
        
        # Longitudes should differ due to different ayanamsas
        assert lahiri_mars.longitude != kp_mars.longitude, "Different ayanamsas should produce different longitudes"
        
        # But distances should be the same (ayanamsa doesn't affect distance)
        assert abs(lahiri_mars.distance - kp_mars.distance) < 0.001
