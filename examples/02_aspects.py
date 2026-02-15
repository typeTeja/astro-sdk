"""
Aspect Calculation Example

This example shows how to calculate aspects between planets
and identify applying vs separating aspects.
"""

from datetime import datetime, timezone
from astrosdk.core.time import Time
from astrosdk.core.ephemeris import Ephemeris
from astrosdk.services.natal_service import NatalService
from astrosdk.services.aspect_service import AspectService

def main():
    # Initialize services
    eph = Ephemeris()
    natal_service = NatalService(eph)
    aspect_service = AspectService()
    
    # Calculate chart for a specific time
    birth_time = Time(datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc))
    
    chart = natal_service.calculate_natal_chart(
        time=birth_time,
        latitude=40.7128,
        longitude=-74.0060
    )
    
    # Calculate aspects
    aspects = aspect_service.calculate_aspects(chart.planets)
    
    # Display aspects
    print("=" * 70)
    print("PLANETARY ASPECTS")
    print("=" * 70)
    print(f"Date: {birth_time.dt}")
    print()
    
    # Group by aspect type
    aspect_types = {}
    for aspect in aspects:
        if aspect.type not in aspect_types:
            aspect_types[aspect.type] = []
        aspect_types[aspect.type].append(aspect)
    
    # Display each type
    for aspect_type in ["CONJUNCTION", "OPPOSITION", "TRINE", "SQUARE", "SEXTILE"]:
        if aspect_type in aspect_types:
            print(f"\n{aspect_type}S")
            print("-" * 70)
            for aspect in aspect_types[aspect_type]:
                applying = "Applying" if aspect.applying else "Separating"
                print(f"{aspect.p1.name:10} {aspect.type:12} {aspect.p2.name:10} "
                      f"(orb: {aspect.orb:4.2f}°) [{applying}]")
    
    # Summary
    print()
    print("=" * 70)
    print(f"Total aspects found: {len(aspects)}")
    print(f"Applying: {sum(1 for a in aspects if a.applying)}")
    print(f"Separating: {sum(1 for a in aspects if not a.applying)}")

if __name__ == "__main__":
    main()
