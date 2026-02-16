"""Tests for Phase 10 Research Tools"""

import pytest
from datetime import datetime, timezone, timedelta
from astrosdk.domain.midpoints import (
    calculate_midpoint, calculate_all_midpoints, find_midpoint_aspects,
    Midpoint, MidpointTree
)
from astrosdk.domain.harmonics import (
    calculate_harmonic_longitude, calculate_harmonic_positions,
    find_harmonic_aspects, HarmonicChart
)
from astrosdk.domain.primary_directions import (
    calculate_primary_direction, calculate_all_primary_directions,
    calculate_firdaria, DirectedPosition
)
from astrosdk.domain.astrocartography import (
    calculate_planetary_line, calculate_astromap,
    PlanetaryLine, AstroMap
)
from astrosdk.domain.planet import PlanetPosition
from astrosdk.core.constants import Planet


def make_planet(planet, longitude):
    """Helper to create planet position."""
    return PlanetPosition(
        planet=planet,
        longitude=longitude,
        latitude=0.0,
        distance=1.0,
        speed_long=0.5,
        speed_lat=0.0,
        speed_dist=0.0
    )


class TestMidpoints:
    """Test midpoint calculations."""
    
    def test_basic_midpoint(self):
        """Calculate midpoint between two longitudes."""
        near, far = calculate_midpoint(0, 90)
        assert near == 45.0
        assert far == 225.0
    
    def test_wraparound_midpoint(self):
        """Midpoint wrapping around 0°."""
        near, far = calculate_midpoint(350, 10)
        assert near == 0.0 or near == 360.0  # Both valid
        assert far == 180.0
    
    def test_all_midpoints(self):
        """Calculate all midpoints for chart."""
        positions = [
            make_planet(Planet.SUN, 100.0),
            make_planet(Planet.MOON, 200.0),
            make_planet(Planet.MERCURY, 150.0)
        ]
        
        tree = calculate_all_midpoints(positions)
        
        # 3 planets = 3 midpoints (SUN/MOON, SUN/MERC, MOON/MERC)
        assert len(tree.midpoints) == 3
        assert all(isinstance(m, Midpoint) for m in tree.midpoints)
    
    def test_midpoint_model(self):
        """Midpoint model properties."""
        mp = Midpoint(
            planet1=Planet.SUN,
            planet2=Planet.MOON,
            planet1_longitude=100.0,
            planet2_longitude=200.0,
            midpoint_longitude=150.0,
            far_midpoint_longitude=330.0
        )
        
        
        assert mp.sign.value == 5  # Virgo (150° / 30 = 5)
        assert mp.sign_degree == 0.0
    
    def test_midpoint_tree_range(self):
        """Get midpoints in longitude range."""
        positions = [
            make_planet(Planet.SUN, 100.0),
            make_planet(Planet.MOON, 200.0),
            make_planet(Planet.VENUS, 50.0)
        ]
        
        tree = calculate_all_midpoints(positions)
        in_range = tree.get_by_longitude_range(140.0, 160.0)
        
        # Sun/Moon midpoint at 150° should be in range
        assert len(in_range) >= 1
    
    def test_find_midpoint_aspects(self):
        """Find midpoints aspecting a target."""
        positions = [
            make_planet(Planet.SUN, 100.0),
            make_planet(Planet.MOON, 200.0)
        ]
        
        tree = calculate_all_midpoints(positions)
        
        # Find midpoints near 150° (Sun/Moon midpoint)
        activated = find_midpoint_aspects(tree.midpoints, 150.0, orb=2.0)
        
        assert len(activated) >= 1


class TestHarmonicCharts:
    """Test harmonic chart calculations."""
    
    def test_harmonic_longitude(self):
        """Calculate harmonic longitude."""
        assert calculate_harmonic_longitude(100.0, 2) == 200.0
        assert calculate_harmonic_longitude(100.0, 5) == 140.0  # (100*5) % 360
        assert calculate_harmonic_longitude(300.0, 3) == 180.0  # (300*3) % 360
    
    def test_harmonic_positions(self):
        """Generate harmonic chart."""
        positions = [
            make_planet(Planet.SUN, 100.0),
            make_planet(Planet.MOON, 200.0)
        ]
        
        h5 = calculate_harmonic_positions(positions, 5)
        
        assert h5.harmonic == 5
        assert len(h5.positions) == 2
        assert h5.get_planet(Planet.SUN) is not None
    
    def test_harmonic_aspects(self):
        """Find conjunctions in harmonic chart."""
        positions = [
            make_planet(Planet.SUN, 72.0),   # 72*5 = 360 = 0°
            make_planet(Planet.MOON, 72.5)   # 72.5*5 = 362.5 = 2.5°
        ]
        
        h5 = calculate_harmonic_positions(positions, 5)
        aspects = find_harmonic_aspects(h5, orb=3.0)
        
        # Sun and Moon should be conjunct in H5
        assert len(aspects) >= 1


class TestPrimaryDirections:
    """Test primary direction calculations."""
    
    def test_direct_direction(self):
        """Direct primary direction."""
        directed = calculate_primary_direction(100.0, 30.0, "direct")
        assert directed == 130.0
    
    def test_converse_direction(self):
        """Converse primary direction."""
        directed = calculate_primary_direction(100.0, 30.0, "converse")
        assert directed == 70.0
    
    def test_all_primary_directions(self):
        """Calculate directions for all planets."""
        positions = [
            make_planet(Planet.SUN, 100.0),
            make_planet(Planet.MOON, 200.0)
        ]
        
        directed = calculate_all_primary_directions(positions, 45.0, "direct")
        
        assert len(directed) == 2
        assert all(isinstance(d, DirectedPosition) for d in directed)
        assert all(d.age_years == 45.0 for d in directed)
    
    def test_firdaria_calculation(self):
        """Calculate Firdaria periods."""
        birth = datetime(1990, 1, 1, 12, 0, tzinfo=timezone.utc)
        
        periods = calculate_firdaria(birth, is_day_birth=True)
        
        assert len(periods) == 7  # 7 planetary periods
        assert periods[0].planet == Planet.SUN  # Day birth starts with Sun
        assert periods[0].start_age == 0.0
        assert periods[0].level == 1


class TestAstroCartography:
    """Test astro-cartography calculations."""
    
    def test_planetary_line(self):
        """Create planetary line."""
        line = calculate_planetary_line(
            Planet.JUPITER,
            150.0,
            20.0,
            "MC"
        )
        
        assert line.planet == Planet.JUPITER
        assert line.line_type == "MC"
        assert line.planet_longitude == 150.0
    
    def test_astromap_generation(self):
        """Generate complete astro-map."""
        positions = [
            make_planet(Planet.SUN, 100.0),
            make_planet(Planet.MOON, 200.0)
        ]
        
        astro_map = calculate_astromap(positions)
        
        # 2 planets × 4 lines each = 8 total lines
        assert len(astro_map.lines) == 8
        assert all(isinstance(line, PlanetaryLine) for line in astro_map.lines)
    
    def test_get_lines_for_planet(self):
        """Get lines for specific planet."""
        positions = [
            make_planet(Planet.SUN, 100.0),
            make_planet(Planet.MOON, 200.0)
        ]
        
        astro_map = calculate_astromap(positions)
        sun_lines = astro_map.get_lines_for_planet(Planet.SUN)
        
        # Sun should have 4 lines (AS, MC, DS, IC)
        assert len(sun_lines) == 4
        assert all(line.planet == Planet.SUN for line in sun_lines)
    
    def test_get_lines_by_type(self):
        """Get lines by angle type."""
        positions = [
            make_planet(Planet.SUN, 100.0),
            make_planet(Planet.MOON, 200.0)
        ]
        
        astro_map = calculate_astromap(positions)
        mc_lines = astro_map.get_lines_by_type("MC")
        
        # Should have 2 MC lines (one for each planet)
        assert len(mc_lines) == 2
        assert all(line.line_type == "MC" for line in mc_lines)


class TestIntegration:
    """Integration tests combining multiple research tools."""
    
    def test_midpoints_and_harmonics(self):
        """Use midpoints in harmonic analysis."""
        positions = [
            make_planet(Planet.SUN, 100.0),
            make_planet(Planet.MOON, 200.0)
        ]
        
        # Calculate midpoint
        tree = calculate_all_midpoints(positions)
        sun_moon_mp = [m for m in tree.midpoints 
                       if {m.planet1, m.planet2} == {Planet.SUN, Planet.MOON}][0]
        
        # Create position at midpoint for harmonic analysis
        mp_position = make_planet(Planet.MERCURY, sun_moon_mp.midpoint_longitude)
        h7 = calculate_harmonic_positions([mp_position], 7)
        
        assert h7.harmonic == 7
        assert len(h7.positions) == 1
