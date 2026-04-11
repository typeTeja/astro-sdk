import pytest
from datetime import datetime, UTC
from app.core.time import Time
from app.core.constants import Planet, ZodiacSign
from app.services.mundane.ingress_service import IngressService
from app.contexts.factories import create_default_context

@pytest.mark.parametrize("planet, start_search, expected_date, expected_sign", [
    (Planet.SATURN, datetime(1991, 1, 1, tzinfo=UTC), "1991-02-06", ZodiacSign.AQUARIUS), # Saturn into Aquarius 1991 (Tropical)
    (Planet.JUPITER, datetime(2021, 12, 1, tzinfo=UTC), "2021-12-29", ZodiacSign.PISCES), # Jupiter into Pisces 2021 (Tropical)
    (Planet.MARS, datetime(2024, 2, 1, tzinfo=UTC), "2024-02-13", ZodiacSign.AQUARIUS), # Mars into Aquarius 2024 (Tropical)
])
def test_historical_ingresses(planet, start_search, expected_date, expected_sign):
    """
    Verify the 2.0 IngressEngine against known historical boundary dates.
    Uses Tropical zodiac for these standard dates.
    """
    context = create_default_context()
    context.zodiac.zodiac = "tropical"
    context.zodiac.sidereal_mode = None
    
    service = IngressService(context)
    
    # Search for a 60-day window from start
    start_time = Time(start_search)
    from datetime import timedelta
    end_time = Time(start_search + timedelta(days=60))
    
    events = service.scan_ingresses(planet, start_time, end_time)
    
    assert len(events) > 0
    hit = events[0]
    assert hit.sign_to == expected_sign
    assert hit.time.strftime("%Y-%m-%d") == expected_date
