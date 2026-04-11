from datetime import datetime, UTC, timedelta
from app.core.time import Time
from app.core.constants import Planet, SiderealMode
from app.contexts.factories import create_default_context
from app.sdk.client import AstroSDKClient

def run_graduation_demo():
    print("=== AstroSDK 2.0 Graduation Demo ===\n")
    
    # 1. Initialize the 2.0 Client with a specific context
    context = create_default_context()
    context.zodiac.sidereal_mode = SiderealMode.LAHIRI
    context.zodiac.zodiac = "sidereal"
    
    client = AstroSDKClient(context)
    print(f"Engine Version: {client.config.feature.engine_version}")
    print(f"Fingerprint: {client.config.feature.fingerprint}\n")
    
    # 2. Western Natal Calculation
    t_birth = Time(datetime(1990, 1, 1, 12, 0, tzinfo=UTC))
    natal = client.western.compute_natal(t_birth, 17.385, 78.486)
    print(f"Natal Moon (Lahiri): {natal.planets[1].longitude:.4f}°")
    
    # 3. Vedic Panchang
    panchang = client.vedic.get_panchang(t_birth, 17.385, 78.486)
    print(f"Vedic Nakshatra: {panchang.nakshatra}\n")
    
    # 4. Mundane Event Scanning (Alpha Feature)
    print("Scanning for upcoming Mars Stations...")
    start_scan = Time.now()
    end_scan = Time.from_julian_day(start_scan.julian_day + 180)
    
    events = client.mundane.scan_events(
        planets=[Planet.MARS],
        start_time=start_scan,
        end_time=end_scan,
        scan_stations=True
    )
    
    for e in events:
        print(f"Event: {e.planet.name} {getattr(e, 'station_type', 'EVENT')} at {e.time.isoformat()}")
        
    print("\n=== Graduation Complete ===")

if __name__ == "__main__":
    run_graduation_demo()
