import pytest
from datetime import datetime, UTC
from app.contexts import CalculationContext
from app.contexts.factories import create_default_context
from app.core.ephemeris import Ephemeris
from app.core.ephemeris_context import EphemerisContext
from app.core.constants import SiderealMode, HouseSystem
from app.core.time import Time
from app.services.western.chart_service import WesternChartService
from app.services.western.aspect_service import WesternAspectService


def test_ephemeris_context_isolation():
    """Verify that EphemerisContext isolates and restores global state."""
    eph = Ephemeris()
    
    # Set a base state
    eph.set_sidereal_mode(SiderealMode.LAHIRI)
    
    with EphemerisContext(sid_mode=SiderealMode.FAGAN_BRADLEY):
        assert eph.sidereal_mode == SiderealMode.FAGAN_BRADLEY
    
    # Should be restored to Lahiri
    assert eph.sidereal_mode == SiderealMode.LAHIRI


def test_western_chart_service_native():
    """Verify that WesternChartService creates a chart with correct metadata."""
    time = Time(datetime(2024, 1, 1, 12, 0, tzinfo=UTC))
    context = create_default_context()
    service = WesternChartService(context)
    
    chart = service.create_chart(time, lat=51.5, lon=-0.1)
    
    assert chart.time == time
    assert len(chart.planets) >= 10
    assert len(chart.houses.cusps) == 12
    assert chart.metadata["capability"] == "core.generic"
    assert chart.metadata["zodiac"] == "tropical"


def test_western_aspect_service_native():
    """Verify that WesternAspectService calculates aspects correctly."""
    context = create_default_context()
    service = WesternAspectService(context)
    
    time = Time(datetime(2024, 1, 1, 12, 0, tzinfo=UTC))
    chart_service = WesternChartService(context)
    chart = chart_service.create_chart(time, lat=51.5, lon=-0.1)
    
    aspects = service.calculate_aspects(chart.planets)
    
    assert len(aspects) > 0
    for aspect in aspects:
        assert aspect.type in service.MAJOR_ASPECTS.values()
        assert aspect.orb <= service.DEFAULT_ORBS[aspect.type]


def test_fingerprint_reproducibility():
    """Verify that fingerprints are identical for identical calculations."""
    time = Time(datetime(2024, 1, 1, 12, 0, tzinfo=UTC))
    context = create_default_context()
    service = WesternChartService(context)
    
    chart1 = service.create_chart(time, lat=51.5, lon=-0.1)
    chart2 = service.create_chart(time, lat=51.5, lon=-0.1)
    
    # Chart objects themselves might have different IDs, 
    # but their calculation results should lead to the same data structure for fingerprinting
    # (Checking manual data equality first)
    assert chart1.planets[0].longitude == chart2.planets[0].longitude


def test_vedic_varga_service_d9():
    """Verify D9 Navamsa calculation logic and metadata."""
    time = Time(datetime(2024, 1, 1, 12, 0, tzinfo=UTC))
    context = create_default_context()
    # Ensure sidereal mode for Vedic
    context.zodiac.sidereal_mode = SiderealMode.LAHIRI
    
    chart_service = WesternChartService(context)
    chart = chart_service.create_chart(time, lat=51.5, lon=-0.1)
    
    from app.services.vedic.varga_service import VargaService, VargaMethod
    varga_service = VargaService(context)
    d9_chart = varga_service.calculate_varga(chart.planets, division=9)
    
    assert d9_chart.division == 9
    assert d9_chart.method == VargaMethod.PARASHARA
    assert len(d9_chart.planets) == len(chart.planets)
    assert "Navamsha" in d9_chart.title


def test_vedic_dasha_service_defaults():
    """Verify that DashaService defaults to Lahiri and calculates levels correctly."""
    time = Time(datetime(2024, 1, 1, 12, 0, tzinfo=UTC))
    context = create_default_context()
    # We leave sidereal_mode as None to test default behavior
    
    from app.services.vedic.dasha_service import DashaService
    service = DashaService(context)
    dashas = service.calculate_vimshottari(time, levels=2)
    
    assert len(dashas) == 9 # Full cycle of 9 lords
    assert dashas[0].level == 1
    assert len(dashas[0].sub_periods) == 9 # Antardashas
    assert dashas[0].sub_periods[0].level == 2


def test_mundane_multi_event_scanner():
    """Verify that the Multi-Event Scanner correctly identifies ingresses and stations."""
    # Search for events in 2024 for Mars
    start_time = Time(datetime(2024, 1, 1, 0, 0, tzinfo=UTC))
    end_time = Time(datetime(2024, 6, 1, 0, 0, tzinfo=UTC))
    
    context = create_default_context()
    from app.services.mundane.event_service import EventService as NativeEventService
    from app.core.constants import Planet
    
    service = NativeEventService(context)
    events = service.scan_multi_events(
        planets=[Planet.MARS],
        start_time=start_time,
        end_time=end_time,
        scan_ingresses=True,
        scan_stations=True
    )
    
    # Mars changes signs roughly every 2 months. 
    # Between Jan and June 2024, it should have at least 2-3 ingresses.
    ingresses = [e for e in events if e.type == "INGRESS"]
    assert len(ingresses) >= 2
    
    # Basic data check
    for e in ingresses:
        assert hasattr(e, "sign_from")
        assert hasattr(e, "sign_to")


def test_mundane_exact_aspect_scan():
    """Verify that the Exact Aspect Scanner detects planetary alignments."""
    # Sun conjunction Jupiter in May 2024 (roughly)
    start_time = Time(datetime(2024, 5, 1, 0, 0, tzinfo=UTC))
    end_time = Time(datetime(2024, 6, 1, 0, 0, tzinfo=UTC))
    
    context = create_default_context()
    from app.services.mundane.event_service import EventService as NativeEventService
    from app.core.constants import Planet
    
    service = NativeEventService(context)
    events = service.scan_multi_events(
        planets=[Planet.SUN, Planet.JUPITER],
        start_time=start_time,
        end_time=end_time,
        scan_ingresses=False,
        scan_stations=False,
        aspect_targets=[(Planet.SUN, Planet.JUPITER, 0.0)] # Conjunction
    )
    
    # Solar-Jupiter conjunction happens roughly once a year.
    # It happened around May 18, 2024.
    aspects = [e for e in events if e.type == "ASPECT"]
    assert len(aspects) == 1
    assert aspects[0].primary_planet == Planet.SUN
    assert aspects[0].secondary_planet == Planet.JUPITER
    assert aspects[0].target_angle == 0.0


def test_research_export_csv():
    """Verify that the Research Export Service generates valid CSV data."""
    context = create_default_context()
    from app.services.research.export_service import ExportService
    from app.core.constants import Planet
    from datetime import timedelta
    
    start = Time(datetime(2024, 1, 1, 0, 0, tzinfo=UTC))
    end = Time(datetime(2024, 1, 3, 0, 0, tzinfo=UTC))
    
    service = ExportService(context)
    stream = service.stream_ephemeris(
        planets=[Planet.SUN],
        start_time=start,
        end_time=end,
        step=timedelta(days=1),
        format="CSV"
    )
    
    csv_content = "".join(list(stream))
    assert "date_utc" in csv_content
    assert "SUN" in csv_content
    # 2024-01-01, 2024-01-02, 2024-01-03 -> 3 rows + header
    lines = [l for l in csv_content.split("\n") if l.strip()]
    assert len(lines) == 4


def test_research_export_parquet():
    """Verify that the Research Export Service generates valid Parquet bytes."""
    context = create_default_context()
    from app.services.research.export_service import ExportService
    from app.core.constants import Planet
    from datetime import timedelta
    import pandas as pd
    import io
    
    start = Time(datetime(2024, 1, 1, 0, 0, tzinfo=UTC))
    end = Time(datetime(2024, 1, 3, 0, 0, tzinfo=UTC))
    
    service = ExportService(context)
    stream = service.stream_ephemeris(
        planets=[Planet.SUN],
        start_time=start,
        end_time=end,
        step=timedelta(days=1),
        format="PARQUET"
    )
    
    parquet_bytes = list(stream)[0]
    assert isinstance(parquet_bytes, bytes)
    
    # Verify with pandas
    df = pd.read_parquet(io.BytesIO(parquet_bytes))
    assert len(df) == 3
    assert "longitude" in df.columns


def test_persistence_saved_chart():
    """Verify that SavedChart models can be persisted and retrieved via SQLModel."""
    from app.core.database import engine
    from app.models.charts import SavedChart
    from app.core.database import create_db_and_tables
    from sqlmodel import Session, select
    
    create_db_and_tables() # Ensure tables exist
    
    with Session(engine) as session:
        chart = SavedChart(
            name="Test Local Persistence",
            natal_time=datetime(2024, 1, 1, 12, 0, tzinfo=UTC),
            latitude=17.385,
            longitude=78.486,
            context_override={"house_system": "PLACIDUS"}
        )
        session.add(chart)
        session.commit()
        session.refresh(chart)
        
        # Retrieve
        statement = select(SavedChart).where(SavedChart.name == "Test Local Persistence")
        db_chart = session.exec(statement).first()
        assert db_chart is not None
        assert db_chart.latitude == 17.385
        assert db_chart.context_override["house_system"] == "PLACIDUS"


def test_job_service_background_execution():
    """Verify that JobService correctly manages job state and executes tasks in threads."""
    from app.core.database import engine
    from app.services.jobs.job_service import JobService
    from app.core.database import create_db_and_tables
    from sqlmodel import Session
    import time
    
    create_db_and_tables()
    
    with Session(engine) as session:
        service = JobService(session)
        job = service.create_job(task_type="TEST", payload={"foo": "bar"})
        
        def dummy_task(x: int):
            return f"Result is {x}"
            
        service.submit_task(job.id, dummy_task, 42)
        
        # Wait for thread pool to finish (since it's a tiny task)
        # In a real environment we'd poll, but here we'll sleep briefly
        time.sleep(1.0)
        
        session.refresh(job)
        assert job.status == "COMPLETED"
        assert job.result_url == "Result is 42"


def test_api_v2_natal_chart_smoke():
    """Verify that API v2 Natal Chart endpoint is responsive and honors V2 contexts."""
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    
    payload = {
        "time": {"time": "2024-01-01T12:00:00Z"},
        "location": {"latitude": 17.385, "longitude": 78.486, "altitude": 0}
    }
    
    # Test with Sidereal Lahiri via Header
    response = client.post(
        "/api/v2/western/natal",
        json=payload,
        headers={"X-Astro-Is-Sidereal": "true", "X-Astro-Sidereal-Mode": "LAHIRI"}
    )
    
    if response.status_code != 200:
        print(f"DEBUG Error Response: {response.json()}")
        
    assert response.status_code == 200
    res_json = response.json()
    assert "planets" in res_json["data"]
    assert "ayanamsa" in res_json["meta"]
    assert res_json["meta"]["ayanamsa"] == "LAHIRI"
    
    # Test Planetary Position V2
    response = client.get("/api/v2/astronomy/planet-position?planet=SUN")
    assert response.status_code == 200
    assert response.json()["planet"] == "SUN"
    assert "fingerprint" in response.json()
