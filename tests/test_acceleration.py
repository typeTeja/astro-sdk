"""
Tests for Planetary Acceleration
"""

import pytest
from astrosdk.domain.planet import PlanetPosition
from astrosdk.domain.acceleration import (
    AccelerationData,
    calculate_acceleration,
    calculate_acceleration_from_ephemeris
)
from astrosdk.core.constants import Planet, SiderealMode
from astrosdk.core.ephemeris import Ephemeris
from astrosdk.core.time import Time


class TestAccelerationCalculation:
    """Test acceleration calculation from position samples."""
    
    def test_positive_acceleration(self):
        """Planet speeding up has positive longitudinal acceleration."""
        # Create three positions with increasing speed
        pos_before = PlanetPosition(
            planet=Planet.MERCURY,
            longitude=100.0,
            latitude=0.0,
            distance=0.7,
            speed_long=1.0,  # Moving at 1°/day
            speed_lat=0.0,
            speed_dist=0.0
        )
        
        pos_current = PlanetPosition(
            planet=Planet.MERCURY,
            longitude=101.0,
            latitude=0.0,
            distance=0.7,
            speed_long=1.5,  # Speeding up to 1.5°/day
            speed_lat=0.0,
            speed_dist=0.0
        )
        
        pos_after = PlanetPosition(
            planet=Planet.MERCURY,
            longitude=102.5,
            latitude=0.0,
            distance=0.7,
            speed_long=2.0,  # Further acceleration to 2°/day
            speed_lat=0.0,
            speed_dist=0.0
        )
        
        accel = calculate_acceleration(pos_before, pos_current, pos_after, time_delta=1.0)
        
        # (2.0 - 1.0) / (2 * 1.0) = 0.5 degrees/day²
        assert accel.longitude_accel == pytest.approx(0.5, abs=0.01)
        assert accel.is_accelerating is True
        assert accel.is_decelerating is False
    
    def test_negative_acceleration_approaching_station(self):
        """Planet slowing down (approaching retrograde station) has negative acceleration."""
        pos_before = PlanetPosition(
            planet=Planet.MARS,
            longitude=120.0,
            latitude=0.0,
            distance=1.5,
            speed_long=0.5,  # Moving forward at 0.5°/day
            speed_lat=0.0,
            speed_dist=0.0
        )
        
        pos_current = PlanetPosition(
            planet=Planet.MARS,
            longitude=120.25,
            latitude=0.0,
            distance=1.5,
            speed_long=0.1,  # Slowing down to 0.1°/day
            speed_lat=0.0,
            speed_dist=0.0
        )
        
        pos_after = PlanetPosition(
            planet=Planet.MARS,
            longitude=120.35,
            latitude=0.0,
            distance=1.5,
            speed_long=-0.1,  # Now retrograde at -0.1°/day
            speed_lat=0.0,
            speed_dist=0.0
        )
        
        accel = calculate_acceleration(pos_before, pos_current, pos_after, time_delta=1.0)
        
        # (-0.1 - 0.5) / (2 * 1.0) = -0.3 degrees/day²
        assert accel.longitude_accel == pytest.approx(-0.3, abs=0.01)
        assert accel.is_decelerating is True
        assert accel.is_accelerating is False
    
    def test_near_station_detection(self):
        """Detect when planet is near a station point (zero acceleration)."""
        pos_before = PlanetPosition(
            planet=Planet.JUPITER,
            longitude=150.0,
            latitude=0.0,
            distance=5.2,
            speed_long=0.005,
            speed_lat=0.0,
            speed_dist=0.0
        )
        
        pos_current = PlanetPosition(
            planet=Planet.JUPITER,
            longitude=150.005,
            latitude=0.0,
            distance=5.2,
            speed_long=0.001,
            speed_lat=0.0,
            speed_dist=0.0
        )
        
        pos_after = PlanetPosition(
            planet=Planet.JUPITER,
            longitude=150.006,
            latitude=0.0,
            distance=5.2,
            speed_long=-0.003,
            speed_lat=0.0,
            speed_dist=0.0
        )
        
        accel = calculate_acceleration(pos_before, pos_current, pos_after, time_delta=1.0)
        
        # Very small acceleration indicates station
        assert accel.is_near_station is True
    
    def test_different_time_delta(self):
        """Acceleration calculation works with different time intervals."""
        pos_before = PlanetPosition(
            planet=Planet.VENUS,
            longitude=200.0,
            latitude=0.0,
            distance=0.7,
            speed_long=1.0,
            speed_lat=0.0,
            speed_dist=0.0
        )
        
        pos_current = PlanetPosition(
            planet=Planet.VENUS,
            longitude=202.0,
            latitude=0.0,
            distance=0.7,
            speed_long=1.5,
            speed_lat=0.0,
            speed_dist=0.0
        )
        
        pos_after = PlanetPosition(
            planet=Planet.VENUS,
            longitude=204.0,
            latitude=0.0,
            distance=0.7,
            speed_long=2.0,
            speed_lat=0.0,
            speed_dist=0.0
        )
        
        # With 2-day interval instead of 1-day
        accel = calculate_acceleration(pos_before, pos_current, pos_after, time_delta=2.0)
        
        # (2.0 - 1.0) / (2 * 2.0) = 0.25 degrees/day²
        assert accel.longitude_accel == pytest.approx(0.25, abs=0.01)


class TestAccelerationFromEphemeris:
    """Test acceleration calculation using real ephemeris data."""
    
    def test_mercury_acceleration_real_data(self):
        """Calculate Mercury's acceleration from ephemeris."""
        from datetime import datetime, timezone
        
        eph = Ephemeris()
        time = Time(datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc))
        
        accel = calculate_acceleration_from_ephemeris(
            ephemeris=eph,
            time=time,
            planet=Planet.MERCURY,
            time_delta_days=1.0
        )
        
        # Basic sanity checks
        assert isinstance(accel, AccelerationData)
        assert isinstance(accel.longitude_accel, float)
        # Mercury's acceleration should be reasonable (not extreme)
        assert -5.0 < accel.longitude_accel < 5.0
    
    def test_jupiter_slow_acceleration(self):
        """Jupiter moves slowly, so acceleration should be small."""
        from datetime import datetime, timezone
        
        eph = Ephemeris()
        time = Time(datetime(2024, 6, 1, 12, 0, tzinfo=timezone.utc))
        
        accel = calculate_acceleration_from_ephemeris(
            ephemeris=eph,
            time=time,
            planet=Planet.JUPITER,
            time_delta_days=1.0
        )
        
        # Jupiter's acceleration should be very small
        assert abs(accel.longitude_accel) < 0.1
    
    def test_sidereal_mode(self):
        """Acceleration calculation works with sidereal mode."""
        from datetime import datetime, timezone
        
        eph = Ephemeris()
        time = Time(datetime(2024, 3, 1, 12, 0, tzinfo=timezone.utc))
        
        accel = calculate_acceleration_from_ephemeris(
            ephemeris=eph,
            time=time,
            planet=Planet.MARS,
            time_delta_days=1.0,
            sidereal_mode=SiderealMode.LAHIRI
        )
        
        assert isinstance(accel, AccelerationData)
        # Acceleration magnitude should be similar in both modes
        assert isinstance(accel.longitude_accel, float)
    
    def test_smaller_time_delta(self):
        """Smaller time delta gives more precise instantaneous acceleration."""
        from datetime import datetime, timezone
        
        eph = Ephemeris()
        time = Time(datetime(2024, 2, 1, 12, 0, tzinfo=timezone.utc))
        
        # Calculate with different time deltas
        accel_1day = calculate_acceleration_from_ephemeris(
            eph, time, Planet.VENUS, time_delta_days=1.0
        )
        
        accel_halfday = calculate_acceleration_from_ephemeris(
            eph, time, Planet.VENUS, time_delta_days=0.5
        )
        
        # Both should be valid
        assert isinstance(accel_1day.longitude_accel, float)
        assert isinstance(accel_halfday.longitude_accel, float)
        
        # They should be similar but not identical
        # (smaller delta gives more precise instantaneous value)
        assert abs(accel_1day.longitude_accel - accel_halfday.longitude_accel) < 1.0
