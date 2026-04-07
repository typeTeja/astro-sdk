import csv
import io
from typing import Iterator

from ..core.constants import Planet, SiderealMode
from ..core.ephemeris import Ephemeris
from ..core.time import Time


class ResearchService:
    """
    High-performance bulk data generation for research.
    Optimized for streaming large datasets (e.g., CSV exports)
    without blowing up memory.
    """

    def __init__(self, ephemeris: Ephemeris) -> None:
        self.eph = ephemeris
        self.ALL_PLANETS = [
            Planet.SUN, Planet.MOON, Planet.MERCURY, Planet.VENUS,
            Planet.MARS, Planet.JUPITER, Planet.SATURN, Planet.URANUS,
            Planet.NEPTUNE, Planet.PLUTO, Planet.TRUE_NODE, Planet.MEAN_NODE,
        ]

    def stream_ephemeris_csv(self, start_time: Time, end_time: Time, step_hours: float = 24.0, is_sidereal: bool = True, sidereal_mode: SiderealMode = SiderealMode.LAHIRI) -> Iterator[str]:
        """
        Yields CSV formatted strings for planetary positions over a time window.
        Uses an Iterator to allow for StreamingResponse downstream.
        """
        from ..core.ephemeris_context import EphemerisContext
        # Create a CSV dict writer writing to an in-memory string buffer
        buffer = io.StringIO()
        
        fieldnames = ["Date(UTC)", "JulianDay", "Planet", "Longitude", "Latitude", "Distance", "SpeedLong", "IsRetrograde"]
        writer = csv.DictWriter(buffer, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        yield buffer.getvalue()
        buffer.seek(0)
        buffer.truncate(0)

        curr_jd = start_time.julian_day
        end_jd = end_time.julian_day
        step_jd = step_hours / 24.0

        if is_sidereal:
            with EphemerisContext(sid_mode=sidereal_mode):
                while curr_jd <= end_jd:
                    t = Time.from_julian_day(curr_jd)
                    for p in self.ALL_PLANETS:
                        pos = self.eph.calculate_planet(t.julian_day, p, sidereal=is_sidereal)
                        
                        writer.writerow({
                            "Date(UTC)": t.dt.isoformat(),
                            "JulianDay": f"{t.julian_day:.6f}",
                            "Planet": p.name,
                            "Longitude": f"{pos['longitude']:.6f}",
                            "Latitude": f"{pos['latitude']:.6f}",
                            "Distance": f"{pos['distance']:.6f}",
                            "SpeedLong": f"{pos['speed_long']:.6f}",
                            "IsRetrograde": str(pos['speed_long'] < 0)
                        })
                    
                    # Yield the chunk
                    yield buffer.getvalue()
                    buffer.seek(0)
                    buffer.truncate(0)
                    
                    curr_jd += step_jd
        else:
            while curr_jd <= end_jd:
                t = Time.from_julian_day(curr_jd)
                for p in self.ALL_PLANETS:
                    pos = self.eph.calculate_planet(t.julian_day, p, sidereal=is_sidereal)
                    
                    writer.writerow({
                        "Date(UTC)": t.dt.isoformat(),
                        "JulianDay": f"{t.julian_day:.6f}",
                        "Planet": p.name,
                        "Longitude": f"{pos['longitude']:.6f}",
                        "Latitude": f"{pos['latitude']:.6f}",
                        "Distance": f"{pos['distance']:.6f}",
                        "SpeedLong": f"{pos['speed_long']:.6f}",
                        "IsRetrograde": str(pos['speed_long'] < 0)
                    })
                
                # Yield the chunk
                yield buffer.getvalue()
                buffer.seek(0)
                buffer.truncate(0)
                
                curr_jd += step_jd
