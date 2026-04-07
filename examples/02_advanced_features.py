"""
Advanced Features Example

This example demonstrates professional-grade features including
Locational Astronomy (Horizon), Planetary Stations, Parans, and Sign Ingresses.
"""

from datetime import UTC, datetime

from app.core.constants import Planet, SiderealMode
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.services.crossing_service import CrossingService
from app.services.heliacal_service import HeliacalService
from app.services.horizon_service import HorizonService
from app.services.natal_service import NatalService
from app.services.paran_service import ParanService


def run_advanced_demo():
    # 1. Initialize Services
    eph = Ephemeris()
    natal_service = NatalService(eph)
    horizon_service = HorizonService(eph)
    heliacal_service = HeliacalService(eph)
    paran_service = ParanService(eph)
    crossing_service = CrossingService(eph)

    # 2. Locational Context (Venice, Italy)
    lat, lon = 45.4408, 12.3155
    now = Time(datetime(2024, 6, 21, 12, 0, tzinfo=UTC))

    print(f"--- Advanced Demo: {now.dt.date()} in Venice ---")
    print("-" * 60)

    # 3. Automatic Horizontal Coordinates
    # NatalService can populate Azimuth/Altitude automatically if geopos is provided
    positions = natal_service.calculate_positions(now, lat=lat, lon=lon)
    sun = next(p for p in positions if p.planet == Planet.SUN)
    print(f"Sun Position:     {sun.longitude:.2f}° Long, {sun.azimuth:.2f}° Az, {sun.altitude:.2f}° Alt")

    # 4. Precise Horizon Events
    # High-precision search for sunrise, solar noon, and sunset
    sunrise = horizon_service.calculate_sunrise(now, lat, lon)
    sunset = horizon_service.calculate_sunset(now, lat, lon)
    solar_noon = horizon_service.calculate_transit(Planet.SUN, now, lat, lon)

    print(f"Sunrise:          {sunrise.dt if sunrise else 'N/A'}")
    print(f"Solar Noon:       {solar_noon.dt if solar_noon else 'N/A'}")
    print(f"Sunset:           {sunset.dt if sunset else 'N/A'}")

    # 5. Specialized Heliacal Events
    # Calculation of "First Visibility" (Heliacal Rising) using Swiss Ephemeris visibility models
    venus_heliacal = heliacal_service.calculate_heliacal_rising(Planet.VENUS, now, lat, lon)
    print(f"Venus Heliacal:   {venus_heliacal.dt if venus_heliacal else 'Not found in search window'}")

    # 6. Yearly Planetary Stations
    # Scan for Direct/Retrograde stations for an entire year
    stations = heliacal_service.find_all_stations(Planet.MERCURY, 2024)
    print("\nMercury Stations 2024:")
    for s in stations[:4]: # Show more stations
        print(f"  {s['time'].dt.date()}: {s['type']} at {s['time'].dt.strftime('%H:%M')} UT")

    # 7. Simultaneous Events (Parans)
    # Finding points where two bodies cross any angle (Asc, Desc, MC, IC) simultaneously
    print("\nParans for today (5 min orb):")
    parans = paran_service.find_parans(now, lat, lon, orb_minutes=5.0)
    for p in parans[:3]:
        print(f"  {p['time'].dt.strftime('%H:%M')} UT: {p['p1'].name} {p['type1']} / {p['p2'].name} {p['type2']}")

    # 8. Sign Ingresses
    # Detecting the exact second a planet crosses into a new zodiac sign
    print("\nNext Sign Ingresses (Lahiri Ayanamsa):")
    for p in [Planet.SUN, Planet.MARS, Planet.JUPITER]:
        ingress_time, sign_num = crossing_service.find_next_ingress(p, now, sidereal_mode=SiderealMode.LAHIRI)
        print(f"  {p.name:10} Ingress: {ingress_time.dt.date()} into Sign {sign_num}")

if __name__ == "__main__":
    run_advanced_demo()
