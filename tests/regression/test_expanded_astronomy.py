import pytest
import os
import sys
from datetime import datetime, timezone

# Add src to sys.path
sys.path.append(os.path.join(os.getcwd(), "src"))

from astrosdk.core.time import Time
from astrosdk.core.constants import Planet
from astrosdk.services.planetary_service import PlanetaryService
from astrosdk.services.fixed_star_service import FixedStarService
from astrosdk.services.event_service import EventService
from astrosdk.core.ephemeris import Ephemeris

def test_planetary_phenomena_venus():
    """Verify Venus phenomena calculation."""
    service = PlanetaryService()
    # 2024-06-04 approx Venus Superior Conjunction
    time = Time.from_string("2024-06-04 00:00:00")
    pheno = service.get_phenomena(Planet.VENUS, time)
    
    assert pheno.planet == Planet.VENUS
    # At superior conjunction, phase fraction is near 1.0
    assert pheno.phase_fraction > 0.99
    assert -5 < pheno.apparent_magnitude < -3

def test_fixed_star_sirius():
    """Verify Sirius position (Sidereal Lahiri)."""
    service = FixedStarService()
    time = Time.from_string("2024-01-01 00:00:00")
    sirius = service.get_star_position("Sirius", time)
    
    assert sirius.name.startswith("Sirius")
    # Sirius is approx 20deg Gemini (Tropical) -> approx 14deg Cancer (Sidereal Lahiri?) 
    # Actually at J2000 it's 14 deg Cancer Tropical.
    # Lahiri is approx -24 deg. 104 - 24 = 80.
    assert 75 < sirius.longitude < 85 
    assert sirius.magnitude < 0 # Sirius is very bright (-1.46)

def test_solar_eclipse_2024():
    """Verify the Great American Eclipse of April 8, 2024."""
    eph = Ephemeris()
    service = EventService(eph)
    start_time = Time.from_string("2024-04-01 00:00:00")
    
    eclipse = service.find_next_solar_eclipse(start_time)
    
    assert eclipse.type == "SOLAR"
    # Check date matches April 8
    t_peak = datetime.fromtimestamp((eclipse.peak_jd - 2440587.5) * 86400.0, tz=timezone.utc)
    assert t_peak.month == 4
    assert t_peak.day == 8
    assert eclipse.magnitude >= 1.0 # Total eclipse

def test_sidereal_time_and_delta_t():
    """Verify precision time utilities."""
    time = Time.from_string("2024-01-01 12:00:00")
    # Delta-T in 2024 is approx 69 seconds
    assert 68/86400 < time.delta_t < 70/86400
    assert 0 <= time.sidereal_time < 24
