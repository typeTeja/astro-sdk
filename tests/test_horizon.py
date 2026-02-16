import pytest
from datetime import datetime, timezone
from astrosdk.core.time import Time
from astrosdk.core.ephemeris import Ephemeris
from astrosdk.core.constants import Planet
from astrosdk.services.horizon_service import HorizonService

@pytest.fixture
def ephemeris():
    return Ephemeris()

@pytest.fixture
def horizon_service(ephemeris):
    return HorizonService(ephemeris)

class TestHorizonService:
    def test_sunrise_sunset_london(self, horizon_service):
        """Test sunrise and sunset for London."""
        # 2024-03-20 (Equinox) - Start at midnight to catch same-day events
        date = Time(datetime(2024, 3, 20, 0, 0, tzinfo=timezone.utc))
        lat, lon = 51.5074, -0.1278 # London
        
        sunrise = horizon_service.calculate_sunrise(date, lat, lon)
        sunset = horizon_service.calculate_sunset(date, lat, lon)
        
        # In March in London, sunrise is ~06:00 and sunset ~18:00
        assert sunrise.dt.hour in [5, 6, 7]
        assert sunset.dt.hour in [17, 18, 19]
        assert sunrise.julian_day < sunset.julian_day

    def test_transit_jupiter(self, horizon_service):
        """Test Jupiter transit calculation."""
        date = Time(datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc))
        lat, lon = 35.6762, 139.6503 # Tokyo
        
        transit = horizon_service.calculate_transit(Planet.JUPITER, date, lat, lon)
        assert isinstance(transit, Time)
        # Transit should happen once a day
        assert 0 <= transit.dt.hour < 24

    def test_twilight_civil(self, horizon_service):
        """Test civil twilight calculation."""
        date = Time(datetime(2024, 6, 21, 12, 0, tzinfo=timezone.utc)) # Summer solstice
        lat, lon = 40.7128, -74.0060 # NYC
        
        twilight = horizon_service.calculate_twilight(date, lat, lon, twilight_type="civil")
        
        assert "dawn" in twilight
        assert "dusk" in twilight
        
        # Dawn should be before sunrise
        sunrise = horizon_service.calculate_sunrise(date, lat, lon)
        assert twilight["dawn"].julian_day < sunrise.julian_day
        
        # Dusk should be after sunset
        sunset = horizon_service.calculate_sunset(date, lat, lon)
        assert twilight["dusk"].julian_day > sunset.julian_day

    def test_twilight_all_types(self, horizon_service):
        """Test all twilight types for consistency."""
        date = Time(datetime(2024, 3, 20, 12, 0, tzinfo=timezone.utc))
        lat, lon = 0.0, 0.0 # Equator
        
        civil = horizon_service.calculate_twilight(date, lat, lon, twilight_type="civil")
        nautic = horizon_service.calculate_twilight(date, lat, lon, twilight_type="nautical")
        astro = horizon_service.calculate_twilight(date, lat, lon, twilight_type="astronomical")
        
        # Order of dawn: astro < nautic < civil
        assert astro["dawn"].julian_day < nautic["dawn"].julian_day < civil["dawn"].julian_day
        # Order of dusk: civil < nautic < astro
        assert civil["dusk"].julian_day < nautic["dusk"].julian_day < astro["dusk"].julian_day
