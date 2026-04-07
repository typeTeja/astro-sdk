import pytest
import pandas as pd
from datetime import datetime, UTC
from app.core.constants import Planet
from app.core.time import Time
from app.core.ephemeris import Ephemeris
from app.services.quant_service import AstroQuantService
from app.engine.quant_engine import QuantEngine


@pytest.fixture
def eph():
    return Ephemeris()

@pytest.fixture
def quant_service(eph):
    return AstroQuantService(eph)

@pytest.fixture
def quant_engine():
    return QuantEngine()

def test_synodic_phase_moon(quant_service):
    # New Moon: 2024-04-08 18:21 UTC (approx)
    t = Time(datetime(2024, 4, 8, 18, 21, tzinfo=UTC))
    cycle = quant_service.calculate_synodic_phase(Planet.SUN, Planet.MOON, t)
    
    # At New Moon, phase should be near 0 or 360
    assert min(cycle.phase, 360.0 - cycle.phase) < 1.0
    # Moon is faster than Sun, so after NM it should be Waxing
    t_after = Time(datetime(2024, 4, 9, 18, 21, tzinfo=UTC))
    cycle_after = quant_service.calculate_synodic_phase(Planet.MOON, Planet.SUN, t_after)
    assert cycle_after.is_waxing is True

def test_velocity_metrics_sun(quant_service):
    t = Time(datetime(2024, 1, 1, 0, 0, tzinfo=UTC))
    metrics = quant_service.calculate_velocity_metrics(Planet.SUN, t)
    
    # Sun velocity is ~0.98 deg/day
    assert 0.9 < metrics.relative_speed < 1.1
    assert metrics.price_mapping >= 0
    assert metrics.price_mapping < 360

def test_quant_engine_dataframe(quant_engine):
    start = Time(datetime(2024, 1, 1, 0, 0, tzinfo=UTC))
    end = Time(datetime(2024, 1, 2, 0, 0, tzinfo=UTC))
    
    df = quant_engine.generate_indicators(
        start, end, interval_minutes=240, # Every 4 hours
        planets=[Planet.SUN, Planet.MOON],
        synodic_pairs=[(Planet.SUN, Planet.MOON)]
    )
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 7 # (24 hours / 4) + 1 = 7 rows
    assert "SUN_velocity" in df.columns
    assert "MOON_velocity" in df.columns
    assert "SUN_MOON_phase" in df.columns
    assert not df.isnull().values.any()

def test_quant_engine_correlation(quant_engine):
    # Dummy price data
    dates = pd.date_range("2024-01-01", periods=10, freq="D", tz="UTC")
    price_df = pd.DataFrame({"close": [100, 101, 102, 101, 100, 99, 98, 99, 100, 101]}, index=dates)
    
    start = Time(datetime(2024, 1, 1, tzinfo=UTC))
    end = Time(datetime(2024, 1, 10, tzinfo=UTC))
    astro_df = quant_engine.generate_indicators(start, end, interval_minutes=1440)
    
    correlations = quant_engine.correlate_with_price(price_df, astro_df)
    assert isinstance(correlations, pd.Series)
    assert len(correlations) > 0
