from datetime import datetime, timezone
from astrosdk.core.time import Time
from astrosdk.core.ephemeris import Ephemeris
from astrosdk.core.constants import Planet, SiderealMode
from astrosdk.services.natal_service import NatalService
from astrosdk.services.horizon_service import HorizonService
from astrosdk.services.heliacal_service import HeliacalService
from astrosdk.services.paran_service import ParanService
from astrosdk.services.crossing_service import CrossingService

def run_advanced_demo():
    # Initialize ephemeris
    eph = Ephemeris()
    natal_service = NatalService(eph)
    horizon_service = HorizonService(eph)
    heliacal_service = HeliacalService(eph)
    paran_service = ParanService(eph)
    crossing_service = CrossingService(eph)

    # 1. Locational Context (Venice, Italy)
    lat, lon = 45.4408, 12.3155
    now = Time(datetime(2024, 6, 21, 12, 0, tzinfo=timezone.utc))

    print(f"--- Advanced Demo: {now.dt} in Venice ---")

    # 2. Horizontal Coordinates
    # NatalService can now take geopos and calculate Azimuth/Altitude automatically
    positions = natal_service.calculate_positions(now, lat=lat, lon=lon)
    sun = next(p for p in positions if p.planet == Planet.SUN)
    print(f"Sun Position: {sun.longitude:.2f}° Long, {sun.azimuth:.2f}° Az, {sun.altitude:.2f}° Alt")
    print(f"Sun Zenith Distance: {sun.zenith_distance:.2f}°")
    print(f"Sun Antiscia: {sun.antiscia:.2f}°")

    # 3. Horizon Events
    sunrise = horizon_service.calculate_sunrise(now, lat, lon)
    sunset = horizon_service.calculate_sunset(now, lat, lon)
    noon = horizon_service.calculate_transit(now, lat, lon)
    
    print(f"Sunrise: {sunrise.dt if sunrise else 'N/A'}")
    print(f"Solar Noon: {noon.dt if noon else 'N/A'}")
    print(f"Sunset: {sunset.dt if sunset else 'N/A'}")

    # 4. Heliacal Rising (First visibility of a body before sunrise)
    venus_rising = heliacal_service.calculate_heliacal_rising(Planet.VENUS, now, lat, lon)
    print(f"Next Venus Heliacal Rising: {venus_rising.dt if venus_rising else 'Not found in window'}")

    # 5. Planetary Stations (Retrograde/Direct points)
    stations = heliacal_service.find_all_stations(Planet.MERCURY, 2024)
    print("\nMercury Stations 2024:")
    for s in stations[:2]: # Show first two
        print(f"  {s['time'].dt.date()}: {s['type']}")

    # 6. Parans (Simultaneous horizon/meridian crossings)
    print("\nParans for today (5 min orb):")
    parans = paran_service.find_parans(now, lat, lon, orb_minutes=5.0)
    for p in parans[:3]:
        print(f"  {p['time'].dt.strftime('%H:%M')} UT: {p['p1'].name} {p['type1']} / {p['p2'].name} {p['type2']}")

    # 7. Ingresses (Sign changes)
    print("\nNext Sign Ingresses:")
    for p in [Planet.SUN, Planet.MARS, Planet.JUPITER]:
        ingress = crossing_service.find_next_ingress(now, p)
        print(f"  {p.name} Ingress: {ingress.dt.date()} at {ingress.dt.strftime('%H:%M')} UT")

if __name__ == "__main__":
    run_advanced_demo()
