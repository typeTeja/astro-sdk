import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, UTC
from app.core.constants import Planet
from app.core.time import Time
from app.engine.quant_engine import QuantEngine


def run_quant_demo():
    print("=" * 60)
    print("AstroSDK Quantitative Research & Correlation Demo")
    print("=" * 60)

    engine = QuantEngine()

    # 1. Define search range (1 year)
    start_time = Time(datetime(2023, 1, 1, tzinfo=UTC))
    end_time = Time(datetime(2024, 1, 1, tzinfo=UTC))
    
    print(f"Generating indicators for {start_time.dt.date()} to {end_time.dt.date()}...")
    
    # 2. Generate Indicators (Daily)
    # We'll track the Sun-Moon cycle (Lunar phases) and Mercury's velocity
    astro_df = engine.generate_indicators(
        start_time, 
        end_time, 
        interval_minutes=1440, # Daily
        planets=[Planet.MERCURY, Planet.MARS, Planet.JUPITER],
        synodic_pairs=[(Planet.SUN, Planet.MOON), (Planet.MARS, Planet.SATURN)]
    )
    
    print(f"Dataset generated: {len(astro_df)} rows.")
    print("\nIndicator Preview (First 5 days):")
    print(astro_df.head())

    # 3. Create a synthetic "Price" series for demo
    # Let's say price correlates slightly with the Lunar Phase (SUN_MOON_phase)
    # New Moon (0) and Full Moon (180) often correspond to pivots in some theories.
    dates = pd.date_range("2023-01-01", "2024-01-01", freq="D", tz=UTC)
    
    # Generate some synthetic noise + a subtle lunar signal
    lunar_signal = np.sin(np.radians(astro_df["SUN_MOON_phase"]))
    noise = np.random.normal(0, 0.5, len(dates))
    price = 100 + np.cumsum(noise + (lunar_signal * 0.2)) # Slight trend following lunar phase
    
    price_df = pd.DataFrame({"close": price}, index=dates)

    # 4. Perform Correlation Analysis
    print("\n" + "-" * 60)
    print("Performing Correlation Analysis with Synthetic Price")
    print("-" * 60)
    
    correlations = engine.correlate_with_price(price_df, astro_df)
    
    # Sort and display meaningful correlations
    sorted_corr = correlations.sort_values(ascending=False)
    print("Correlations with Price Returns:")
    for indicator, value in sorted_corr.items():
        print(f"  {indicator:25}: {value:7.4f}")

    print("\nDemo Completed Successfully.")
    print("Note: In a real research environment, you would replace price_df with data from a CSV or API.")

if __name__ == "__main__":
    run_quant_demo()
