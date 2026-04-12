from datetime import datetime, UTC
from app.core.time import Time
from app.core.ephemeris import Ephemeris
from app.core.constants import Planet
from app.contexts.calculation import CalculationContext
from app.contexts.coordinate import CoordinateSystem
from app.contexts.observer import ObserverContext
from app.contexts.factories import create_default_context
from app.services.astronomy.planetary_service import AstronomyPlanetaryService

def run_verification():
    ephemeris = Ephemeris()
    print("=== AstroSDK 2.0 Engine Integrity Report ===")
    
    # 1. Geocentric Verification (2024 Solar Eclipse)
    ctx_geo = create_default_context()
    time = Time(datetime(2024, 4, 8, 18, 20, 48, tzinfo=UTC))
    service_geo = AstronomyPlanetaryService(ctx_geo, ephemeris)
    pos = service_geo.calculate_positions(time, [Planet.SUN, Planet.MOON])
    diff = abs(pos[0].longitude - pos[1].longitude)
    if diff > 180: diff = 360 - diff
    print(f"[GEOCENTRIC] Sun/Moon Gap:  {diff:.6f}° (Expected < 0.001°)")

    # 2. Topocentric Verification (Mexico Totality Path)
    ctx_topo = create_default_context()
    ctx_topo.coordinate.system = CoordinateSystem.TOPOCENTRIC
    ctx_topo.observer = ObserverContext(latitude=25.3, longitude=-104.1, altitude=0)
    service_topo = AstronomyPlanetaryService(ctx_topo, ephemeris)
    pos_topo = service_topo.calculate_positions(time, [Planet.SUN, Planet.MOON])
    diff_topo = abs(pos_topo[0].longitude - pos_topo[1].longitude)
    if diff_topo > 180: diff_topo = 360 - diff_topo
    print(f"[TOPOCENTRIC] Sun/Moon Gap: {diff_topo:.6f}° (Expected < 0.01° @ Totality)")

    # 3. Heliocentric Verification
    ctx_helio = create_default_context()
    ctx_helio.coordinate.system = CoordinateSystem.HELIOCENTRIC
    service_helio = AstronomyPlanetaryService(ctx_helio, ephemeris)
    pos_helio = service_helio.calculate_positions(time, [Planet.VENUS]) # Sun is 0 in helio usually
    print(f"[HELIOCENTRIC] Venus Longitude: {pos_helio[0].longitude:.6f}°")

if __name__ == "__main__":
    run_verification()
