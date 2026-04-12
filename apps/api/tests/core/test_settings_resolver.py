import pytest
from app.schemas.settings import ChartSettings
from app.core.settings_resolver import resolve_settings
from app.core.constants import SiderealMode, HouseSystem

def test_tropical_wipes_ayanamsa():
    """If zodiac is tropical, ayanamsa must be wiped (None)."""
    settings = ChartSettings(
        zodiac="tropical",
        sidereal_mode=SiderealMode.LAHIRI
    )
    resolved = resolve_settings(settings)
    assert resolved.zodiac == "tropical"
    assert resolved.sidereal_mode is None

def test_sidereal_mandates_ayanamsa():
    """If zodiac is sidereal and ayanamsa is missing, it should fallback to Lahiri."""
    settings = ChartSettings(
        zodiac="sidereal",
        sidereal_mode=None
    )
    resolved = resolve_settings(settings)
    assert resolved.zodiac == "sidereal"
    assert resolved.sidereal_mode == SiderealMode.LAHIRI

def test_heliocentric_wipes_houses():
    """Heliocentric calculations should not have house systems."""
    settings = ChartSettings(
        coordinate_system="heliocentric",
        house_system=HouseSystem.PLACIDUS
    )
    resolved = resolve_settings(settings)
    assert resolved.coordinate_system == "heliocentric"
    assert resolved.house_system is None

def test_no_aspect_system_wipes_orb():
    """If no aspect system is set, orb should be None."""
    settings = ChartSettings(
        aspect_system=None,
        orb=5.0
    )
    resolved = resolve_settings(settings)
    assert resolved.orb is None

def test_aspect_system_keeps_orb():
    """If aspect system is set, orb should be preserved."""
    settings = ChartSettings(
        aspect_system="western",
        orb=5.0
    )
    resolved = resolve_settings(settings)
    assert resolved.orb == 5.0
