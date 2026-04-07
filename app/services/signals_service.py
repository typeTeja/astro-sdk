import math
from datetime import timedelta

from ..core.constants import Planet, SiderealMode
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..domain.signals import AstroIntensity, ClusterIndex
from .aspect_service import AspectService
from .natal_service import NatalService


class SignalsService:
    """
    Non-predictive quantitative analysis of the astrological state space.
    Calculates statistical density metrics like aspect intensity and stelliums.
    """

    def __init__(self, ephemeris: Ephemeris) -> None:
        self.eph = ephemeris
        self.natal_service = NatalService(self.eph)
        self.aspect_service = AspectService()
        self.MAJOR_PLANETS = [
            Planet.SUN, Planet.MOON, Planet.MERCURY, Planet.VENUS,
            Planet.MARS, Planet.JUPITER, Planet.SATURN, Planet.URANUS,
            Planet.NEPTUNE, Planet.PLUTO
        ]

    def calculate_intensity(self, start_time: Time, end_time: Time, step_hours: int = 24) -> list[AstroIntensity]:
        """
        Produce a time-series of Astro Intensity scores.
        Score is derived from the number of active major aspects and their orb tightness.
        Exactly 0 orb = high contribution, edge of orb = low contribution.
        """
        results: list[AstroIntensity] = []
        curr_jd = start_time.julian_day
        end_jd = end_time.julian_day
        step_jd = step_hours / 24.0

        while curr_jd <= end_jd:
            t = Time.from_julian_day(curr_jd)
            chart_planets = self.natal_service.calculate_positions(t, SiderealMode.LAHIRI)
            filtered_planets = [p for p in chart_planets if p.planet in self.MAJOR_PLANETS]

            # We use global orb of None to use default classical orbs for scanning
            aspects = self.aspect_service.calculate_aspects(filtered_planets)

            score = 0.0
            contributors = []
            
            for aspect in aspects:
                # Closer orb = higher score. Max 10 per aspect perfectly exact.
                # Assuming max standard orb is ~10 degrees.
                weight = max(0, 10.0 - aspect.orb)
                score += weight
                contributors.append({
                    "aspect": f"{aspect.p1.name} {aspect.type} {aspect.p2.name}",
                    "orb": aspect.orb,
                    "contribution": weight,
                })

            # Sort contributors by most impact
            contributors.sort(key=lambda x: float(x["contribution"]), reverse=True)

            score_capped = min(100.0, score * 1.5) # Scale factor to normalize to 0-100 roughly

            results.append(
                AstroIntensity(
                    time=t.dt,
                    score=round(score_capped, 2),
                    active_aspects_count=len(aspects),
                    top_contributors=contributors[:5], # Keep top 5
                )
            )

            curr_jd += step_jd

        return results

    def calculate_cluster_index(self, start_time: Time, end_time: Time, orb_degrees: float = 10.0, step_hours: int = 24) -> list[ClusterIndex]:
        """
        Finds 'Stelliums' or dense clusters of 3+ planets within a rolling orb window.
        """
        results: list[ClusterIndex] = []
        curr_jd = start_time.julian_day
        end_jd = end_time.julian_day
        step_jd = step_hours / 24.0

        while curr_jd <= end_jd:
            t = Time.from_julian_day(curr_jd)
            chart_planets = self.natal_service.calculate_positions(t, SiderealMode.LAHIRI)
            filtered = [p for p in chart_planets if p.planet in self.MAJOR_PLANETS]
            
            # Sort by longitude
            filtered.sort(key=lambda x: x.longitude)

            clusters = []
            n = len(filtered)
            
            # Simple sliding window for clusters
            i = 0
            while i < n:
                current_cluster = [filtered[i]]
                j = i + 1
                
                # Check circular wrap for the end of the array isn't handled here for simplicity
                # assuming 10 degree window doesn't cross 355 to 5 perfectly in this naive scan
                # To handle wrap, we could double the array with +360 offsets.
                
                while j < n and (filtered[j].longitude - filtered[i].longitude) <= orb_degrees:
                    current_cluster.append(filtered[j])
                    j += 1
                
                if len(current_cluster) >= 3:
                    center = sum(p.longitude for p in current_cluster) / len(current_cluster)
                    span = current_cluster[-1].longitude - current_cluster[0].longitude
                    clusters.append({
                        "center_longitude": center,
                        "span_degrees": span,
                        "planets": [p.planet for p in current_cluster]
                    })
                    i = j # Skip ahead
                else:
                    i += 1

            # Determine density score based on number of planets in clusters
            score = sum(len(c["planets"]) for c in clusters) * 10.0

            results.append(
                ClusterIndex(
                    time=t.dt,
                    stellar_density_score=min(100.0, score),
                    clusters=clusters,
                )
            )

            curr_jd += step_jd

        return results
