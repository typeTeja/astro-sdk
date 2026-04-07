"""
Aspect Calculation Example

This example demonstrates how to calculate aspects between planets
using the new 20-aspect family filtering and custom orbs.
"""

from datetime import UTC, datetime

from app.core.time import Time
from app.engine.chart_engine import ChartEngine
from app.services.aspect_service import AspectService


def main():
    # 1. Initialize services
    engine = ChartEngine()
    aspect_service = AspectService()

    # 2. Calculate chart for a specific time
    # (High-level engine handles positions and houses)
    event_time = Time(datetime(2024, 3, 20, 3, 6, tzinfo=UTC)) # Aries Ingress

    chart = engine.create_chart(
        time=event_time,
        lat=51.5074,
        lon=-0.1278 # London
    )

    # 3. Calculate Major Aspects (Ptolemaic)
    print("=" * 70)
    print("MAJOR ASPECTS (5 Original)")
    print("=" * 70)
    major_aspects = aspect_service.calculate_aspects(chart.planets, aspect_types=['major'])
    display_aspects(major_aspects)

    # 4. Calculate Minor + Kepler Aspects
    print("\n" + "=" * 70)
    print("MINOR & KEPLER ASPECTS")
    print("=" * 70)
    advanced_aspects = aspect_service.calculate_aspects(
        chart.planets,
        aspect_types=['minor', 'kepler']
    )
    display_aspects(advanced_aspects)

    # 5. Calculate ALL 20 Aspect Types with Custom Orbs
    # This includes Septile, Novile, and Undecile families
    print("\n" + "=" * 70)
    print("ALL 20 ASPECTS (Septile/Novile/Undecile families)")
    print("=" * 70)
    all_aspects = aspect_service.calculate_aspects(
        chart.planets,
        aspect_types=['all'],
        custom_orbs={"CONJUNCTION": 12.0, "SEXTILE": 8.0}
    )
    display_aspects(all_aspects)

def display_aspects(aspects):
    if not aspects:
        print("No aspects found.")
        return

    for aspect in sorted(aspects, key=lambda a: a.orb):
        applying = "Applying" if aspect.applying else "Separating"
        print(f"{aspect.p1.name:10} {aspect.type:15} {aspect.p2.name:10} "
              f"(Orb: {aspect.orb:4.2f}°) [{applying}]")

if __name__ == "__main__":
    main()
