"""
Test all aspects and ayanamsas.
"""
import pytest
from datetime import datetime, timezone
from astrosdk.core.time import Time
from astrosdk.core.constants import Planet, SiderealMode
from astrosdk.core.ephemeris import Ephemeris
from astrosdk.services.natal_service import NatalService
from astrosdk.services.aspect_service import AspectService


@pytest.fixture
def ephemeris():
    """Shared ephemeris instance."""
    return Ephemeris()


@pytest.fixture
def natal_service(ephemeris):
    """Shared natal service instance."""
    return NatalService(ephemeris)



class TestAllAspects:
    """Test all aspect types."""
    
    def test_major_aspects(self, natal_service):
        """Test major (Ptolemaic) aspects."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        planets = natal_service.calculate_positions(time)
        
        aspect_service = AspectService()
        aspects = aspect_service.calculate_aspects(planets, aspect_types=['major'])
        
        # Should find some major aspects
        assert len(aspects) > 0
        
        # All aspects should be major types
        major_types = {"CONJUNCTION", "SEXTILE", "SQUARE", "TRINE", "OPPOSITION"}
        for aspect in aspects:
            assert aspect.type in major_types
    
    def test_minor_aspects(self, natal_service):
        """Test minor aspects."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        planets = natal_service.calculate_positions(time)
        
        aspect_service = AspectService()
        aspects = aspect_service.calculate_aspects(planets, aspect_types=['minor'])
        
        # Minor aspects exist but may not always be found
        minor_types = {"SEMI-SEXTILE", "SEMI-SQUARE", "SESQUI-QUADRATE", "QUINCUNX"}
        for aspect in aspects:
            assert aspect.type in minor_types
    
    def test_kepler_aspects(self, natal_service):
        """Test Kepler (quintile family) aspects."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        planets = natal_service.calculate_positions(time)
        
        aspect_service = AspectService()
        aspects = aspect_service.calculate_aspects(planets, aspect_types=['kepler'])
        
        kepler_types = {"QUINTILE", "BIQUINTILE"}
        for aspect in aspects:
            assert aspect.type in kepler_types
    
    def test_all_aspects(self, natal_service):
        """Test all aspect types combined."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        planets = natal_service.calculate_positions(time)
        
        aspect_service = AspectService()
        aspects = aspect_service.calculate_aspects(planets, aspect_types=['all'])
        
        # Should find more aspects when including all types
        assert len(aspects) > 0
    
    def test_custom_orbs(self, natal_service):
        """Test custom orb configuration."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        planets = natal_service.calculate_positions(time)
        
        aspect_service = AspectService()
        
        # Very tight orbs
        tight_aspects = aspect_service.calculate_aspects(
            planets, 
            aspect_types=['major'],
            custom_orbs={"CONJUNCTION": 1.0, "TRINE": 1.0, "SQUARE": 1.0, "OPPOSITION": 1.0, "SEXTILE": 1.0}
        )
        
        # Wide orbs
        wide_aspects = aspect_service.calculate_aspects(
            planets,
            aspect_types=['major'],
            custom_orbs={"CONJUNCTION": 15.0, "TRINE": 15.0, "SQUARE": 15.0, "OPPOSITION": 15.0, "SEXTILE": 15.0}
        )
        
        # Wide orbs should find more or equal aspects
        assert len(wide_aspects) >= len(tight_aspects)
    
    def test_aspect_orb_accuracy(self, natal_service):
        """Test that aspect orbs are calculated correctly."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        planets = natal_service.calculate_positions(time)
        
        aspect_service = AspectService()
        aspects = aspect_service.calculate_aspects(planets, aspect_types=['all'])
        
        for aspect in aspects:
            # Orb should be within the configured limit
            orb_limit = aspect_service.DEFAULT_ORBS.get(aspect.type, 0.0)
            assert aspect.orb <= orb_limit


class TestAllAyanamsas:
    """Test all ayanamsa systems."""
    
    def test_lahiri_ayanamsa(self, natal_service):
        """Test Lahiri ayanamsa (Indian government standard)."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        planets = natal_service.calculate_positions(time, sidereal_mode=SiderealMode.LAHIRI)
        
        assert len(planets) > 0
        # Lahiri should give different positions than tropical
        sun = next(p for p in planets if p.planet == Planet.SUN)
        assert sun.longitude is not None
    
    def test_fagan_bradley_ayanamsa(self, natal_service):
        """Test Fagan/Bradley ayanamsa (Western sidereal)."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        planets = natal_service.calculate_positions(time, sidereal_mode=SiderealMode.FAGAN_BRADLEY)
        
        assert len(planets) > 0
        sun = next(p for p in planets if p.planet == Planet.SUN)
        assert sun.longitude is not None
    
    def test_krishnamurti_ayanamsa(self, natal_service):
        """Test Krishnamurti (KP) ayanamsa."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        planets = natal_service.calculate_positions(time, sidereal_mode=SiderealMode.KRISHNAMURTI)
        
        assert len(planets) > 0
        sun = next(p for p in planets if p.planet == Planet.SUN)
        assert sun.longitude is not None
    
    def test_raman_ayanamsa(self, natal_service):
        """Test B.V. Raman ayanamsa."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        planets = natal_service.calculate_positions(time, sidereal_mode=SiderealMode.RAMAN)
        
        assert len(planets) > 0
        sun = next(p for p in planets if p.planet == Planet.SUN)
        assert sun.longitude is not None
    
    def test_yukteshwar_ayanamsa(self, natal_service):
        """Test Sri Yukteshwar ayanamsa."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        planets = natal_service.calculate_positions(time, sidereal_mode=SiderealMode.YUKTESHWAR)
        
        assert len(planets) > 0
        sun = next(p for p in planets if p.planet == Planet.SUN)
        assert sun.longitude is not None
    
    def test_galactic_center_ayanamsa(self, natal_service):
        """Test Galactic Center at 0 Sagittarius ayanamsa."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        planets = natal_service.calculate_positions(time, sidereal_mode=SiderealMode.GALCENT_0SAG)
        
        assert len(planets) > 0
        sun = next(p for p in planets if p.planet == Planet.SUN)
        assert sun.longitude is not None
    
    def test_j2000_ayanamsa(self, natal_service):
        """Test J2000 ayanamsa."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        planets = natal_service.calculate_positions(time, sidereal_mode=SiderealMode.J2000)
        
        assert len(planets) > 0
        sun = next(p for p in planets if p.planet == Planet.SUN)
        assert sun.longitude is not None
    
    def test_different_ayanamsas_give_different_positions(self, natal_service):
        """Test that different ayanamsas produce different positions."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        
        # Calculate with different ayanamsas
        lahiri_planets = natal_service.calculate_positions(time, sidereal_mode=SiderealMode.LAHIRI)
        fagan_planets = natal_service.calculate_positions(time, sidereal_mode=SiderealMode.FAGAN_BRADLEY)
        krishnamurti_planets = natal_service.calculate_positions(time, sidereal_mode=SiderealMode.KRISHNAMURTI)
        
        # Get Sun positions
        lahiri_sun = next(p for p in lahiri_planets if p.planet == Planet.SUN)
        fagan_sun = next(p for p in fagan_planets if p.planet == Planet.SUN)
        krishnamurti_sun = next(p for p in krishnamurti_planets if p.planet == Planet.SUN)
        
        # Positions should be different (within reasonable bounds)
        assert abs(lahiri_sun.longitude - fagan_sun.longitude) > 0.1
        assert abs(lahiri_sun.longitude - krishnamurti_sun.longitude) > 0.01
    
    def test_vedic_ayanamsas(self, natal_service):
        """Test various Vedic/Hindu ayanamsa systems."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        
        vedic_modes = [
            SiderealMode.SURYASIDDHANTA,
            SiderealMode.ARYABHATA,
            SiderealMode.TRUE_CITRA,
            SiderealMode.TRUE_REVATI,
            SiderealMode.TRUE_PUSHYA
        ]
        
        for mode in vedic_modes:
            planets = natal_service.calculate_positions(time, sidereal_mode=mode)
            assert len(planets) > 0
            sun = next(p for p in planets if p.planet == Planet.SUN)
            assert sun.longitude is not None
    
    def test_babylonian_ayanamsas(self, natal_service):
        """Test Babylonian ayanamsa systems."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        
        babylonian_modes = [
            SiderealMode.BABYLONIAN_KUGLER1,
            SiderealMode.BABYLONIAN_KUGLER2,
            SiderealMode.BABYLONIAN_HUBER,
            SiderealMode.BABYLONIAN_ETPSC,
            SiderealMode.BABYLONIAN_BRITTON
        ]
        
        for mode in babylonian_modes:
            planets = natal_service.calculate_positions(time, sidereal_mode=mode)
            assert len(planets) > 0
            sun = next(p for p in planets if p.planet == Planet.SUN)
            assert sun.longitude is not None
    
    def test_galactic_ayanamsas(self, natal_service):
        """Test galactic-based ayanamsa systems."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        
        galactic_modes = [
            SiderealMode.GALCENT_0SAG,
            SiderealMode.GALCENT_RGILBRAND,
            SiderealMode.GALEQU_IAU1958,
            SiderealMode.GALEQU_TRUE,
            SiderealMode.GALCENT_COCHRANE
        ]
        
        for mode in galactic_modes:
            planets = natal_service.calculate_positions(time, sidereal_mode=mode)
            assert len(planets) > 0
            sun = next(p for p in planets if p.planet == Planet.SUN)
            assert sun.longitude is not None
