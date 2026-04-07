import pandas as pd

from ..core.constants import Planet
from ..core.ephemeris import Ephemeris
from ..core.time import Time
from ..services.quant_service import AstroQuantService


class QuantEngine:
    """
    High-level engine for generating research-ready datasets
    and performing correlation analysis.
    """

    def __init__(self) -> None:
        """Initialize the quantitative engine."""
        self.eph = Ephemeris()
        self.quant_service = AstroQuantService(self.eph)

    def generate_indicators(
        self,
        start_time: Time,
        end_time: Time,
        interval_minutes: int = 60,
        planets: list[Planet] | None = None,
        synodic_pairs: list[tuple[Planet, Planet]] | None = None,
    ) -> pd.DataFrame:
        """
        Generate a Pandas DataFrame with astrological indicators over a range.
        """
        if planets is None:
            planets = [Planet.SUN, Planet.MOON, Planet.MERCURY]
        if synodic_pairs is None:
            synodic_pairs = [(Planet.SUN, Planet.MOON)]
        data = []
        current_jd = start_time.julian_day
        end_jd = end_time.julian_day
        step_jd = interval_minutes / 1440.0

        timestamps = []
        while current_jd <= end_jd:
            t = Time.from_julian_day(current_jd)
            timestamps.append(t.dt)

            row = {}
            # 1. Individual Planet Metrics
            for p in planets:
                metrics = self.quant_service.calculate_velocity_metrics(p, t)
                row[f"{p.name}_velocity"] = metrics.relative_speed
                row[f"{p.name}_acceleration"] = metrics.speed_roc

            # 2. Synodic Pairs
            for p1, p2 in synodic_pairs:
                cycle = self.quant_service.calculate_synodic_phase(p1, p2, t)
                row[f"{p1.name}_{p2.name}_phase"] = cycle.phase

            data.append(row)
            current_jd += step_jd

        df = pd.DataFrame(data, index=timestamps)
        df.index.name = "timestamp"
        return df

    def correlate_with_price(
        self, price_df: pd.DataFrame, astro_df: pd.DataFrame, price_col: str = "close"
    ) -> pd.Series:
        """
        Calculate correlations between price movements and astrological indicators.
        Automatically aligns dataframes by timestamp.
        """
        # Ensure common timezone and alignment
        merged = pd.merge_asof(
            price_df.sort_index(),
            astro_df.sort_index(),
            left_index=True,
            right_index=True,
            direction="nearest",
        )

        # Calculate returns if not already present
        if f"{price_col}_returns" not in merged.columns:
            merged[f"{price_col}_returns"] = merged[price_col].pct_change()

        correlations = merged.corr()[f"{price_col}_returns"].drop(
            [price_col, f"{price_col}_returns"]
        )
        return correlations
