"""
Tests for KP House System
"""

import pytest
from astrosdk.domain.kp_houses import (
    KPCusp,
    KPHouseSystem,
    get_nakshatra_lord,
    get_sub_lord,
    get_sign_lord,
    calculate_kp_houses,
    NAKSHATRA_LORDS
)
from astrosdk.core.constants import Planet, ZodiacSign


class TestNakshatraLords:
    """Test nakshatra (lunar mansion) lord calculations."""
    
    def test_ashwini_nakshatra(self):
        """First nakshatra (Ashwini) ruled by Ketu."""
        # 0° to 13°20' = Ashwini
        assert get_nakshatra_lord(0.0) == -1  # KETU
        assert get_nakshatra_lord(6.0) == -1
        assert get_nakshatra_lord(13.0) == -1
    
    def test_bharani_nakshatra(self):
        """Second nakshatra (Bharani) ruled by Venus."""
        # 13°20' to 26°40' = Bharani
        assert get_nakshatra_lord(13.5) == Planet.VENUS
        assert get_nakshatra_lord(20.0) == Planet.VENUS
    
    def test_krittika_nakshatra(self):
        """Third nakshatra (Krittika) ruled by Sun."""
        # 26°40' to 40° (spans Aries/Taurus) = Krittika
        assert get_nakshatra_lord(27.0) == Planet.SUN
        assert get_nakshatra_lord(35.0) == Planet.SUN
    
    def test_rohini_nakshatra(self):
        """Fourth nakshatra (Rohini) ruled by Moon."""
        # 40° to 53°20' = Rohini
        assert get_nakshatra_lord(40.5) == Planet.MOON
        assert get_nakshatra_lord(50.0) == Planet.MOON
    
    def test_nakshatra_cycle(self):
        """27 nakshatras cycle correctly."""
        # There are 27 nakshatras total
        assert len(NAKSHATRA_LORDS) == 27
        
        # Should cycle back after 360°
        assert get_nakshatra_lord(0.0) == get_nakshatra_lord(360.0)
        
        # Verify different points
        lords_at_degrees = [get_nakshatra_lord(i * 30.0) for i in range(12)]
        # Should have variety (not all the same)
        assert len(set(lords_at_degrees)) > 1


class TestSubLords:
    """Test sub-lord calculations using Vimshottari proportions."""
    
    def test_early_degree_ketu(self):
        """Very early degrees should be Ketu sub-lord."""
        # First sub-division in any nakshatra
        sub = get_sub_lord(0.5)
        assert sub == -1  # KETU
    
    def test_sub_lord_is_valid_planet(self):
        """Sub-lord should always be one of the 9 planets."""
        valid_planets = {
            -1, Planet.VENUS, Planet.SUN, Planet.MOON,  # -1 is KETU
            Planet.MARS, Planet.MEAN_NODE, Planet.JUPITER, Planet.SATURN,  # MEAN_NODE is RAHU
            Planet.MERCURY
        }
        
        # Test various degrees
        for deg in [0, 5, 15, 45, 90, 180, 270, 359]:
            sub = get_sub_lord(float(deg))
            assert sub in valid_planets
    
    def test_sub_lords_vary_within_nakshatra(self):
        """Different positions within same nakshatra have different sub-lords."""
        # Sample positions within first nakshatra (0-13.33°)
        subs = [
            get_sub_lord(0.5),
            get_sub_lord(5.0),
            get_sub_lord(10.0),
            get_sub_lord(13.0)
        ]
        
        # Should have at least 2 different sub-lords
        assert len(set(subs)) >= 2


class TestSignLords:
    """Test zodiac sign rulership."""
    
    def test_aries_mars(self):
        """Aries ruled by Mars."""
        assert get_sign_lord(ZodiacSign.ARIES) == Planet.MARS
    
    def test_taurus_venus(self):
        """Taurus ruled by Venus."""
        assert get_sign_lord(ZodiacSign.TAURUS) == Planet.VENUS
    
    def test_leo_sun(self):
        """Leo ruled by Sun."""
        assert get_sign_lord(ZodiacSign.LEO) == Planet.SUN
    
    def test_cancer_moon(self):
        """Cancer ruled by Moon."""
        assert get_sign_lord(ZodiacSign.CANCER) == Planet.MOON
    
    def test_all_signs_have_lords(self):
        """All 12 signs have rulers."""
        for sign in ZodiacSign:
            lord = get_sign_lord(sign)
            assert isinstance(lord, Planet)


class TestKPCusp:
    """Test KP cusp model."""
    
    def test_kp_cusp_creation(self):
        """Create a KP cusp with all lords."""
        cusp = KPCusp(
            house_number=1,
            longitude=15.5,
            sign_lord=Planet.MARS,
            star_lord=Planet.VENUS,
            sub_lord=Planet.SUN
        )
        
        assert cusp.house_number == 1
        assert cusp.longitude == 15.5
        assert cusp.sign == ZodiacSign.ARIES
        assert cusp.degree_in_sign == pytest.approx(15.5, abs=0.01)
    
    def test_kp_cusp_sign_calculation(self):
        """Cusp correctly calculates its zodiac sign."""
        # 45° = 15° Taurus
        cusp = KPCusp(
            house_number=2,
            longitude=45.0,
            sign_lord=Planet.VENUS,
            star_lord=Planet.MOON,
            sub_lord=Planet.MARS
        )
        
        assert cusp.sign == ZodiacSign.TAURUS
        assert cusp.degree_in_sign == pytest.approx(15.0, abs=0.01)


class TestKPHouseSystem:
    """Test complete KP house system."""
    
    def test_calculate_kp_houses(self):
        """Calculate KP houses from Placidus cusps."""
        # Mock Placidus cusps (30° apart for simplicity)
        placidus_cusps = [i * 30.0 for i in range(12)]
        
        kp_system = calculate_kp_houses(
            house_cusps=placidus_cusps,
            ascendant=0.0,
            midheaven=270.0
        )
        
        assert len(kp_system.cusps) == 12
        assert kp_system.ascendant == 0.0
        assert kp_system.midheaven == 270.0
    
    def test_kp_house_indexing(self):
        """Access KP houses by 1-indexed number."""
        cusps = [i * 30.0 for i in range(12)]
        kp_system = calculate_kp_houses(cusps, 0.0, 270.0)
        
        # 1-indexed access
        first_house = kp_system[1]
        assert first_house.house_number == 1
        assert first_house.longitude == 0.0
        
        twelfth_house = kp_system[12]
        assert twelfth_house.house_number == 12
    
    def test_kp_houses_have_all_lords(self):
        """Each KP cusp has sign, star, and sub-lords."""
        cusps = [15.0 + i * 30.0 for i in range(12)]
        kp_system = calculate_kp_houses(cusps, 15.0, 285.0)
        
        for cusp in kp_system.cusps:
            assert isinstance(cusp.sign_lord, Planet)
            assert isinstance(cusp.star_lord, Planet)
            assert isinstance(cusp.sub_lord, Planet)
    
    def test_kp_invalid_cusp_count(self):
        """Reject invalid number of cusps."""
        with pytest.raises(ValueError, match="Expected 12 house cusps"):
            calculate_kp_houses([0.0, 30.0], 0.0, 270.0)
    
    def test_kp_house_immutability(self):
        """KP house system is immutable."""
        cusps = [i * 30.0 for i in range(12)]
        kp_system = calculate_kp_houses(cusps, 0.0, 270.0)
        
        # Should not be able to modify
        with pytest.raises(Exception):  # Pydantic ValidationError
            kp_system.ascendant = 15.0


class TestKPIntegration:
    """Integration tests for KP system."""
    
    def test_realistic_chart(self):
        """Test with realistic chart cusps."""
        # Approximate cusps for 40.7°N, 74°W at noon
        realistic_cusps = [
            15.5,   # House 1 (Ascendant)
            45.2,   # House 2
            75.8,   # House 3
            105.3,  # House 4 (IC)
            135.1,  # House 5
            165.7,  # House 6
            195.5,  # House 7 (Descendant)
            225.2,  # House 8
            255.8,  # House 9
            285.3,  # House 10 (MC)
            315.1,  # House 11
            345.7,  # House 12
        ]
        
        kp_system = calculate_kp_houses(
            house_cusps=realistic_cusps,
            ascendant=15.5,
            midheaven=285.3
        )
        
        # Verify structure
        assert kp_system[1].longitude == pytest.approx(15.5, abs=0.1)
        assert kp_system[10].longitude == pytest.approx(285.3, abs=0.1)
        
        # All houses have different longitudes
        longitudes = [c.longitude for c in kp_system.cusps]
        assert len(set(longitudes)) == 12
    
    def test_kp_significators_vary(self):
        """Different cusps should have different significators."""
        cusps = [i * 27.5 for i in range(12)]  # Spread across zodiac
        kp_system = calculate_kp_houses(cusps, 0.0, 270.0)
        
        sign_lords = {c.sign_lord for c in kp_system.cusps}
        star_lords = {c.star_lord for c in kp_system.cusps}
        sub_lords = {c.sub_lord for c in kp_system.cusps}
        
        # Should have variety in rulership
        assert len(sign_lords) > 3
        assert len(star_lords) > 3
        assert len(sub_lords) > 2
