"""Tests for Synodic Cycles, Intensity, Declination, and Ephemeris Export"""

import pytest
from datetime import datetime, timezone
from astrosdk.domain.synodic import (
    SynodicCycle, SynodicPhase, calculate_phase_angle, classify_phase
)
from astrosdk.domain.intensity import calculate_intensity, IntensitySignal
from astrosdk.domain.declination import find_declination_aspects, DeclinationAspect
from astrosdk.domain.ephemeris_export import export_ephemeris_csv, export_ephemeris_json
from astrosdk.domain.planet import PlanetPosition
from astrosdk.domain.aspect import Aspect
from astrosdk.core.constants import Planet
from pathlib import Path


class TestSynodicCycles:
    """Test synodic cycle calculations."""
    
    def test_phase_angle_calculation(self):
        """Calculate angular separation correctly."""
        assert calculate_phase_angle(0, 90) == 90.0
        assert calculate_phase_angle(0, 180) == 180.0
        assert calculate_phase_angle(350, 10) == 20.0
        assert calculate_phase_angle(10, 350) == 340.0
    
    def test_classify_phase(self):
        """Classify synodic phases correctly."""
        assert classify_phase(0) == "conjunction"
        assert classify_phase(45) == "waxing_crescent"
        assert classify_phase(90) == "first_quarter"
        assert classify_phase(135) == "waxing_gibbous"
        assert classify_phase(180) == "opposition"
        assert classify_phase(225) == "waning_gibbous"
        assert classify_phase(270) == "last_quarter"
        assert classify_phase(315) == "waning_crescent"
    
    def test_synodic_cycle_model(self):
        """Synodic cycle model works correctly."""
        cycle = SynodicCycle(
            planet1=Planet.SUN,
            planet2=Planet.MOON,
            start_conjunction=datetime(2024, 1, 1, tzinfo=timezone.utc),
            end_conjunction=datetime(2024, 1, 29, tzinfo=timezone.utc),
            phases=[
                SynodicPhase(
                    phase_name="first_quarter",
                    phase_angle=90.0,
                    timestamp=datetime(2024, 1, 8, tzinfo=timezone.utc),
                    planet1_longitude=100.0,
                    planet2_longitude=190.0
                )
            ],
            cycle_length_days=29.5
        )
        
        assert cycle.is_complete is True
        assert len(cycle.phases) == 1


class TestIntensitySignal:
    """Test astrological intensity calculations."""
    
    def make_planet(self, planet, longitude, speed_long=0.5):
        """Helper to create planet position."""
        return PlanetPosition(
            planet=planet,
            longitude=longitude,
            latitude=0.0,
            distance=1.0,
            speed_long=speed_long,
            speed_lat=0.0,
            speed_dist=0.0
        )
    
    def make_aspect(self, p1, p2, orb=2.0):
        """Helper to create aspect."""
        return Aspect(
            p1=p1,
            p2=p2,
            angle=120.0,
            orb=orb,
            type="trine",
            applying=True
        )
    
    def test_low_intensity(self):
        """Low activity period."""
        planets = [
            self.make_planet(Planet.SUN, 100.0, speed_long=1.0),
            self.make_planet(Planet.MOON, 200.0, speed_long=13.0)
        ]
        aspects = []
        
        intensity = calculate_intensity(
            datetime.now(timezone.utc),
            planets, aspects
        )
        
        assert intensity.activity_level == "quiet"
        assert intensity.normalized_value < 0.25
    
    def test_high_intensity(self):
        """High activity period with multiple factors."""
        planets = [
            self.make_planet(Planet.SUN, 100.0),
            self.make_planet(Planet.MOON, 200.0, speed_long=-12.0),  # Retrograde
            self.make_planet(Planet.MERCURY, 150.0, speed_long=-0.8),  # Retrograde
            self.make_planet(Planet.VENUS, 250.0, speed_long=0.02),  # Station
        ]
        
        aspects = [
            self.make_aspect(Planet.SUN, Planet.MOON, orb=0.5),
            self.make_aspect(Planet.SUN, Planet.MERCURY, orb=0.3),
            self.make_aspect(Planet.MOON, Planet.VENUS, orb=0.8),
            self.make_aspect(Planet.MERCURY, Planet.VENUS, orb=0.2),
        ]
        
        intensity = calculate_intensity(
            datetime.now(timezone.utc),
            planets, aspects
        )
        
        assert intensity.retrograde_count == 2
        assert intensity.station_count == 1
        assert intensity.tight_aspect_count >= 2
        assert intensity.activity_level in ["active", "extremely_active"]


class TestDeclinationAspects:
    """Test declination parallels and contra-parallels."""
    
    def make_planet(self, planet, longitude, latitude):
        """Helper to create planet with latitude."""
        return PlanetPosition(
            planet=planet,
            longitude=longitude,
            latitude=latitude,
            distance=1.0,
            speed_long=0.5,
            speed_lat=0.0,
            speed_dist=0.0
        )
    
    def test_parallel_detection(self):
        """Detect parallel aspects (same sign declination)."""
        planets = [
            self.make_planet(Planet.SUN, 100.0, latitude=20.0),
            self.make_planet(Planet.MOON, 200.0, latitude=20.5)
        ]
        
        parallels = find_declination_aspects(planets, orb=1.0)
        
        assert len(parallels) == 1
        assert parallels[0].aspect_type == "parallel"
        assert parallels[0].orb <= 1.0
    
    def test_contra_parallel_detection(self):
        """Detect contra-parallel aspects (opposite sign declination)."""
        planets = [
            self.make_planet(Planet.SUN, 100.0, latitude=20.0),
            self.make_planet(Planet.VENUS, 150.0, latitude=-20.5)
        ]
        
        parallels = find_declination_aspects(planets, orb=1.0)
        
        assert len(parallels) == 1
        assert parallels[0].aspect_type == "contra_parallel"
        assert parallels[0].orb <= 1.0
    
    def test_no_aspects_outside_orb(self):
        """No aspects when beyond orb."""
        planets = [
            self.make_planet(Planet.SUN, 100.0, latitude=20.0),
            self.make_planet(Planet.MOON, 200.0, latitude=10.0)  # 10° difference
        ]
        
        parallels = find_declination_aspects(planets, orb=5.0)
        
        assert len(parallels) == 0


class TestEphemerisExport:
    """Test ephemeris export functionality."""
    
    def test_csv_export_structure(self, tmp_path):
        """CSV export creates correct file structure."""
        output = tmp_path / "test.csv"
        
        def mock_callback(dt, planet):
            return PlanetPosition(
                planet=planet,
                longitude=100.0,
                latitude=0.0,
                distance=1.0,
                speed_long=0.5,
                speed_lat=0.0,
                speed_dist=0.0
            )
        
        result = export_ephemeris_csv(
            start=datetime(2024, 1, 1, tzinfo=timezone.utc),
            end=datetime(2024, 1, 2, tzinfo=timezone.utc),
            planets=[Planet.SUN],
            output_path=str(output),
            interval_days=1.0,
            get_positions_callback=mock_callback
        )
        
        assert Path(result).exists()
        content = Path(result).read_text()
        assert "Date,Time,Planet,Longitude" in content
        assert "SUN" in content
    
    def test_json_export_structure(self, tmp_path):
        """JSON export creates correct file structure."""
        import json
        output = tmp_path / "test.json"
        
        def mock_callback(dt, planet):
            return PlanetPosition(
                planet=planet,
                longitude=100.0,
                latitude=0.0,
                distance=1.0,
                speed_long=0.5,
                speed_lat=0.0,
                speed_dist=0.0
            )
        
        result = export_ephemeris_json(
            start=datetime(2024, 1, 1, tzinfo=timezone.utc),
            end=datetime(2024, 1, 2, tzinfo=timezone.utc),
            planets=[Planet.SUN],
            output_path=str(output),
            interval_days=1.0,
            get_positions_callback=mock_callback
        )
        
        assert Path(result).exists()
        data = json.loads(Path(result).read_text())
        assert "start" in data
        assert "data" in data
        assert len(data["data"]) == 2  # 2 days
