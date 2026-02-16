import pytest
from datetime import datetime, timezone
from astrosdk.core.time import Time
from astrosdk.core.ephemeris import Ephemeris
from astrosdk.core.constants import Planet
from astrosdk.services.paran_service import ParanService
from astrosdk.services.natal_service import NatalService

@pytest.fixture
def ephemeris():
    return Ephemeris()

@pytest.fixture
def natal_service(ephemeris):
    return NatalService(ephemeris)

@pytest.fixture
def paran_service(ephemeris):
    return ParanService(ephemeris)

class TestParansAndAntiscia:
    def test_antiscia_calculation(self, natal_service):
        """Test antiscia and contra-antiscia for Sun."""
        # 2024-03-20 (Aries Ingress ~0°)
        date = Time(datetime(2024, 3, 20, 3, 6, tzinfo=timezone.utc))
        pos = natal_service.calculate_positions(date, sidereal_mode=None)
        sun = next(p for p in pos if p.planet == Planet.SUN)
        
        # At 0° Aries, antiscia is at 180° Virgo. Contra is at 0° Aries.
        assert sun.longitude < 1.0 or sun.longitude > 359.0
        assert 179 <= sun.antiscia < 181
        assert (sun.contra_antiscia < 1.0 or sun.contra_antiscia > 359)

    def test_parans_london(self, paran_service):
        """Test finding parans in London."""
        # A day with many events
        date = Time(datetime(2024, 3, 20, tzinfo=timezone.utc))
        lat, lon = 51.5074, -0.1278 # London
        
        parans = paran_service.find_parans(date, lat, lon)
        
        # Parans should be found (Sun Rise/Set etc)
        assert len(parans) > 0
        
        for p in parans:
            assert isinstance(p["p1"], Planet)
            assert isinstance(p["p2"], Planet)
            assert p["orb_minutes"] <= 5.0
            assert isinstance(p["time"], Time)

    def test_antiscia_mirroring(self, natal_service):
        """Test that antiscia mirrors Cancer/Capricorn correctly."""
        # Planet at 60° (Gemini 0°) -> Antiscia 120° (Leo 0°)
        date = Time(datetime(2024, 6, 1, tzinfo=timezone.utc))
        pos = natal_service.calculate_positions(date)
        # Find any planet and check logic
        p = pos[0]
        assert (p.longitude + p.antiscia) % 360 == pytest.approx(180.0)
        assert (p.longitude + p.contra_antiscia) % 360 == pytest.approx(0.0)
