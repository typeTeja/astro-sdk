import pytest
from datetime import datetime
from zoneinfo import ZoneInfo
from astrosdk.core.time import Time
from astrosdk.core.constants import Planet, SiderealMode, HouseSystem
from astrosdk.engine.chart_engine import ChartEngine

def test_time_strictness():
    # Test strict UTC handling
    with pytest.raises(Exception):
        Time(datetime.now()) # Naive should fail

    t = Time.from_string("2024-01-01 12:00:00", tz="UTC")
    assert t.julian_day > 2460000

def test_chart_calculation():
    engine = ChartEngine()
    
    # Test Date: 2024-01-01 00:00 UTC
    # Location: Greenwich (0, 51.5)
    t = Time.from_string("2024-01-01 00:00:00")
    
    chart = engine.create_chart(t, lat=51.5, lon=0.0, sidereal_mode=SiderealMode.LAHIRI)
    
    # Verify Sun Position (Sidereal Sagittarius approx 16 deg)
    sun = next(p for p in chart.planets if p.planet == Planet.SUN)
    # Tropical Sun is ~10 Cap. Ayanamsa ~24 deg. 
    # 280 (10 Cap) - 24 = 256 (16 Sag).
    
    assert 250 < sun.longitude < 265
    assert sun.planet == Planet.SUN

def test_houses():
    engine = ChartEngine()
    t = Time.from_string("2024-01-01 00:00:00")
    chart = engine.create_chart(t, lat=51.5, lon=0.0)
    
    assert len(chart.houses.cusps) == 12
    assert chart.houses.axes.ascendant > 0
