"""
Tests for Combustion and Essential Dignities
"""

import pytest
from astrosdk.domain.planet import PlanetPosition
from astrosdk.domain.combustion import (
    CombustionState, 
    calculate_combustion,
    is_combust,
    CAZIMI_ORB
)
from astrosdk.domain.dignity import (
    DignityType,
    calculate_dignity,
    get_dignity_score
)
from astrosdk.core.constants import Planet, ZodiacSign


class TestCombustion:
    """Test combustion detection logic."""
    
    def test_cazimi_exact_conjunction(self):
        """Planet within 17 arcminutes (0.283°) is cazimi."""
        result = calculate_combustion(
            planet_longitude=120.0,
            sun_longitude=120.1,  # 0.1° = 6 arcminutes
            planet=Planet.MERCURY
        )
        assert result.state == CombustionState.CAZIMI
        assert result.is_cazimi is True
        assert result.orb_from_sun < CAZIMI_ORB
    
    def test_combust_mercury(self):
        """Mercury 5° from Sun is combust."""
        result = calculate_combustion(
            planet_longitude=125.0,
            sun_longitude=120.0,
            planet=Planet.MERCURY
        )
        assert result.state == CombustionState.COMBUST
        assert result.is_cazimi is False
        assert result.orb_from_sun == 5.0
    
    def test_under_beams(self):
        """Planet 15° from Sun is under the beams."""
        result = calculate_combustion(
            planet_longitude=135.0,
            sun_longitude=120.0,
            planet=Planet.JUPITER  # Jupiter threshold is 11°
        )
        assert result.state == CombustionState.UNDER_BEAMS
        assert result.orb_from_sun == 15.0
    
    def test_free_from_sun(self):
        """Planet 25° from Sun is free."""
        result = calculate_combustion(
            planet_longitude=145.0,
            sun_longitude=120.0,
            planet=Planet.MARS
        )
        assert result.state == CombustionState.FREE
        assert result.orb_from_sun == 25.0
    
    def test_combustion_wraparound(self):
        """Combustion calculation handles 0°/360° boundary."""
        result = calculate_combustion(
            planet_longitude=355.0,  # Near end of zodiac
            sun_longitude=5.0,       # Near start
            planet=Planet.MARS       # Mars has 17° threshold, so 10° is combust
        )
        # Shortest arc is 10°
        assert result.orb_from_sun == 10.0
        assert result.state == CombustionState.COMBUST
    
    def test_custom_threshold(self):
        """Can override default combustion threshold."""
        result = calculate_combustion(
            planet_longitude=128.0,
            sun_longitude=120.0,
            planet=Planet.SATURN,
            custom_threshold=5.0  # Stricter than default 15°
        )
        # 8° from sun, with 5° threshold = under beams
        assert result.state == CombustionState.UNDER_BEAMS
        assert result.threshold_used == 5.0
    
    def test_planet_position_combustion_method(self):
        """PlanetPosition.calculate_combustion integration."""
        mercury = PlanetPosition(
            planet=Planet.MERCURY,
            longitude=125.0,
            latitude=0.0,
            distance=0.7,
            speed_long=1.0,
            speed_lat=0.0,
            speed_dist=0.0
        )
        
        result = mercury.calculate_combustion(sun_longitude=120.0)
        assert result.state == CombustionState.COMBUST


class TestDignities:
    """Test essential dignity classification."""
    
    def test_sun_exalted_aries(self):
        """Sun exalted in Aries (exact at 19°)."""
        # At exact degree
        result = calculate_dignity(Planet.SUN, ZodiacSign.ARIES, 19.0)
        assert result.type == DignityType.EXALTATION
        assert result.strength == 100.0
        assert result.exact_degree == 19.0
        
        # 3° away from exact = 85% strength
        result = calculate_dignity(Planet.SUN, ZodiacSign.ARIES, 16.0)
        assert result.type == DignityType.EXALTATION
        assert result.strength == 85.0
    
    def test_venus_own_sign_taurus(self):
        """Venus in Taurus (own sign)."""
        result = calculate_dignity(Planet.VENUS, ZodiacSign.TAURUS, 15.0)
        assert result.type == DignityType.OWN_SIGN
        assert result.strength == 75.0
    
    def test_mars_in_fall_cancer(self):
        """Mars in fall in Cancer (exact at 28°)."""
        result = calculate_dignity(Planet.MARS, ZodiacSign.CANCER, 28.0)
        assert result.type == DignityType.FALL
        assert result.strength <= 15.0
        assert result.exact_degree == 28.0
    
    def test_saturn_in_detriment_cancer(self):
        """Saturn in detriment in Cancer."""
        result = calculate_dignity(Planet.SATURN, ZodiacSign.CANCER, 10.0)
        assert result.type == DignityType.DETRIMENT
        assert result.strength == 25.0
    
    def test_neutral_placement(self):
        """Planet in neutral sign."""
        result = calculate_dignity(Planet.JUPITER, ZodiacSign.TAURUS, 10.0)
        assert result.type == DignityType.NEUTRAL
        assert result.strength == 50.0
    
    def test_mulatrikona_sun_leo(self):
        """Sun in mulatrikona range in Leo (0-20°)."""
        result = calculate_dignity(Planet.SUN, ZodiacSign.LEO, 10.0, include_mulatrikona=True)
        assert result.type == DignityType.MULATRIKONA
        assert result.strength == 80.0
    
    def test_mulatrikona_out_of_range(self):
        """Sun in Leo > 20° is own sign, not mulatrikona."""
        result = calculate_dignity(Planet.SUN, ZodiacSign.LEO, 25.0, include_mulatrikona=True)
        assert result.type == DignityType.OWN_SIGN
        assert result.strength == 75.0
    
    def test_planet_position_dignity_method(self):
        """PlanetPosition.get_dignity integration."""
        # Sun at 130° = 10° Leo
        sun = PlanetPosition(
            planet=Planet.SUN,
            longitude=130.0,
            latitude=0.0,
            distance=1.0,
            speed_long=1.0,
            speed_lat=0.0,
            speed_dist=0.0
        )
        
        dignity = sun.get_dignity()
        assert dignity.type == DignityType.OWN_SIGN
        
        # With mulatrikona
        dignity_mt = sun.get_dignity(include_mulatrikona=True)
        assert dignity_mt.type == DignityType.MULATRIKONA
    
    def test_get_dignity_score_helper(self):
        """Test simple score helper function."""
        score = get_dignity_score(Planet.SUN, ZodiacSign.ARIES, 19.0)
        assert score == 100.0  # Exaltation
        
        score = get_dignity_score(Planet.MARS, ZodiacSign.CANCER, 28.0)
        assert score <= 15.0  # Fall


class TestCombinedAnalysis:
    """Integration tests combining combustion and dignity."""
    
    def test_cazimi_and_exalted(self):
        """Planet can be cazimi AND exalted (very powerful)."""
        # Sun at 19° Aries (exalted)
        # Mercury exactly conjunct
        sun_long = 19.0  # Aries
        mercury_long = 19.05  # Within cazimi orb
        
        mercury = PlanetPosition(
            planet=Planet.MERCURY,
            longitude=mercury_long,
            latitude=0.0,
            distance=0.7,
            speed_long=1.0,
            speed_lat=0.0,
            speed_dist=0.0
        )
        
        combustion = mercury.calculate_combustion(sun_long)
        assert combustion.state == CombustionState.CAZIMI
        
        # Mercury exalted in Virgo (15°), so in Aries it's neutral
        dignity = mercury.get_dignity()
        assert dignity.type == DignityType.NEUTRAL
