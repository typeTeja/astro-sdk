import pytest
from astrosdk.core.constants import Planet, ZodiacSign
from astrosdk.domain.planet import PlanetPosition
from astrosdk.domain.house import HouseCusp, HouseAxes
from astrosdk.domain.aspect import Aspect

def test_planet_position_immutability():
    p = PlanetPosition(
        planet=Planet.SUN,
        longitude=0.0,
        latitude=0.0,
        distance=1.0,
        speed_long=1.0,
        speed_lat=0.0,
        speed_dist=0.0
    )
    with pytest.raises(Exception):
        p.longitude = 10.0 # Should fail for frozen dataclass

def test_sign_calculation():
    # 0 = Aries, 30 = Taurus, 359 = Pisces
    p1 = PlanetPosition(Planet.SUN, 0.5, 0, 0, 0, 0, 0)
    assert p1.sign == ZodiacSign.ARIES
    
    p2 = PlanetPosition(Planet.MOON, 359.9, 0, 0, 0, 0, 0)
    assert p2.sign == ZodiacSign.PISCES

def test_retrograde():
    p = PlanetPosition(Planet.MERCURY, 100, 0, 0, -0.5, 0, 0)
    assert p.is_retrograde is True
    
    p2 = PlanetPosition(Planet.MERCURY, 100, 0, 0, 0.5, 0, 0)
    assert p2.is_retrograde is False

def test_house_cusp_sign():
    cusp = HouseCusp(1, 45.0) # 15 Taurus
    assert cusp.sign == ZodiacSign.TAURUS

def test_aspect_dataclass():
    a = Aspect(Planet.SUN, Planet.MOON, 120.0, 1.0, "TRINE", True)
    assert a.type == "TRINE"
