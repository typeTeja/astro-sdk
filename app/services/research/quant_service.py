from typing import Any, cast

from app.contexts import CalculationContext
from app.core.constants import Planet
from app.core.ephemeris import Ephemeris
from app.core.time import Time
from app.domain.common.metadata import DomainMetadata


class ResearchQuantService:
    """
    Native 2.0 service for quantitative signals and technical data series.
    """
    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def calculate_intensity(self, start_time: Time, end_time: Time, step_hours: int = 24) -> list[Any]:
        """
        Produce a time-series of Astro Intensity scores in 2.0.
        """
        from app.domain.research.signals import AidenIntensityRecord
        from app.services.western.aspect_service import WesternAspectService
        from app.services.western.chart_service import WesternChartService

        aspect_service = WesternAspectService(self.context)
        chart_service = WesternChartService(self.context, ephemeris=self._eph)

        results = []
        curr_jd = start_time.julian_day
        end_jd = end_time.julian_day
        step_jd = step_hours / 24.0

        major_planets = [Planet.SUN, Planet.MOON, Planet.MERCURY, Planet.VENUS, Planet.MARS, Planet.JUPITER, Planet.SATURN]

        while curr_jd <= end_jd:
            t = Time.from_julian_day(curr_jd)
            # We use a dummy lat/lon as intensity for scanning is usually geocentric/global
            chart = chart_service.create_chart(t, 0.0, 0.0)
            target_planets = [p for p in chart.planets if p.planet in major_planets]

            aspects = aspect_service.calculate_aspects(target_planets)
            score = sum(max(0, 10.0 - a.orb) for a in aspects)

            contributors = [
                {"aspect": f"{a.p1.name} {a.type} {a.p2.name}", "orb": a.orb, "contribution": max(0, 10.0 - a.orb)}
                for a in aspects
            ]
            contributors.sort(key=lambda x: cast("float", x["contribution"]), reverse=True)

            results.append(AidenIntensityRecord(
                time=t.dt,
                score=round(min(100.0, score * 1.5), 2),
                active_aspects_count=len(aspects),
                top_contributors=contributors[:5],
                metadata=DomainMetadata(
                    capability="research.quant.intensity",
                    maturity=self.context.feature.maturity.value,
                    fingerprint=self.context.fingerprint
                )
            ))
            curr_jd += step_jd
        return results

    def calculate_cluster_index(self, start_time: Time, end_time: Time, orb_degrees: float = 10.0, step_hours: int = 24) -> list[Any]:
        """
        Finds 'Stelliums' or dense clusters in 2.0.
        """
        from app.domain.research.signals import ClusterIndexRecord, StellarCluster
        from app.services.western.chart_service import WesternChartService

        chart_service = WesternChartService(self.context, ephemeris=self._eph)
        results = []
        curr_jd = start_time.julian_day
        end_jd = end_time.julian_day
        step_jd = step_hours / 24.0

        major_planets = [Planet.SUN, Planet.MOON, Planet.MERCURY, Planet.VENUS, Planet.MARS, Planet.JUPITER, Planet.SATURN]

        while curr_jd <= end_jd:
            t = Time.from_julian_day(curr_jd)
            chart = chart_service.create_chart(t, 0.0, 0.0)
            pts = [p for p in chart.planets if p.planet in major_planets]
            pts.sort(key=lambda x: x.longitude)

            clusters = []
            i = 0
            while i < len(pts):
                curr = [pts[i]]
                j = i + 1
                while j < len(pts) and (pts[j].longitude - pts[i].longitude) <= orb_degrees:
                    curr.append(pts[j])
                    j += 1

                if len(curr) >= 3:
                    clusters.append(StellarCluster(
                        center_longitude=sum(p.longitude for p in curr) / len(curr),
                        span_degrees=curr[-1].longitude - curr[0].longitude,
                        planets=[p.planet.name for p in curr]
                    ))
                    i = j
                else:
                    i += 1

            results.append(ClusterIndexRecord(
                time=t.dt,
                stellar_density_score=min(100.0, len(clusters) * 30.0), # Simplified heuristic
                clusters=clusters,
                metadata=DomainMetadata(
                    capability="research.quant.cluster",
                    maturity=self.context.feature.maturity.value,
                    fingerprint=self.context.fingerprint
                )
            ))
            curr_jd += step_jd
        return results

    def calculate_synodic_phase(self, p1: Planet, p2: Planet, time: Time) -> Any:
        """
        Calculates relative angle and applying/separating status.
        """
        from app.services.astronomy.synodic_service import AstronomySynodicService
        svc = AstronomySynodicService(self.context, ephemeris=self._eph)
        res = svc.calculate_phase(p1, p2, time)

        from dataclasses import dataclass
        @dataclass
        class Result:
            phase: float
            is_applying: bool

        return Result(phase=res["angle"], is_applying=res["is_applying"])

    def get_velocity_signals(self, planet: Planet, time: Time) -> Any:
        """
        Calculates speed and acceleration indicators.
        """
        pos = self._eph.calculate_planet(time.julian_day, planet)
        # Simple velocity extraction from domain/SE
        from dataclasses import dataclass
        @dataclass
        class VelocityResult:
            speed: float
            acceleration: float

        return VelocityResult(speed=pos["speed_long"], acceleration=0.0) # Acceleration stubbed for now
