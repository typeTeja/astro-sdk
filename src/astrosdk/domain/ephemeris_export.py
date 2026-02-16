"""
Ephemeris Export Tools

Generate CSV and JSON ephemeris tables for research, backtesting,
and data science applications.

Example:
    # Export 1-year daily ephemeris to CSV
    export_ephemeris_csv(
        start=datetime(2024, 1, 1),
        end=datetime(2025, 1, 1),
        planets=[Planet.SUN, Planet.MOON, Planet.MERCURY],
        output_path="ephemeris_2024.csv",
        interval_days=1.0
    )
"""

import csv
import json
from typing import List, Optional
from datetime import datetime, timedelta
from pathlib import Path

from ..core.constants import Planet
from .planet import PlanetPosition


def export_ephemeris_csv(
    start: datetime,
    end: datetime,
    planets: List[Planet],
    output_path: str,
    interval_days: float = 1.0,
    get_positions_callback = None
) -> str:
    """
    Export ephemeris data to CSV format.
    
    Args:
        start: Start date/time
        end: End date/time
        planets: List of planets to include
        output_path: Path to output CSV file
        interval_days: Time interval in days (default 1.0 = daily)
        get_positions_callback: Function(datetime, planet) -> PlanetPosition
                                Must be provided to get positions
    
    Returns:
        Path to created CSV file
    
    CSV Format:
        Date,Time,Planet,Longitude,Latitude,Speed,Sign
        2024-01-01,00:00,SUN,280.12,0.00,1.02,CAPRICORN
        ...
    
    Example:
        >>> def get_pos(dt, planet):
        >>>     chart = calculate_natal_chart(dt, 0, 0)
        >>>     for p in chart.planets:
        >>>         if p.planet == planet:
        >>>             return p
        >>> 
        >>> export_ephemeris_csv(
        >>>     start, end,
        >>>     [Planet.SUN, Planet.MOON],
        >>>     "ephemeris.csv",
        >>>     get_positions_callback=get_pos
        >>> )
    """
    if get_positions_callback is None:
        raise ValueError("get_positions_callback must be provided")
    
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Date', 'Time', 'Planet', 'Longitude', 'Latitude',
            'Speed_Long', 'Speed_Lat', 'Speed_Dist', 'Sign', 'Sign_Degree'
        ])
        
        current = start
        delta = timedelta(days=interval_days)
        
        while current <= end:
            for planet in planets:
                pos = get_positions_callback(current, planet)
                if pos:
                    writer.writerow([
                        current.date().isoformat(),
                        current.time().isoformat(),
                        planet.name,
                        f"{pos.longitude:.6f}",
                        f"{pos.latitude:.6f}",
                        f"{pos.speed_long:.6f}",
                        f"{pos.speed_lat:.6f}",
                        f"{pos.speed_dist:.6f}",
                        pos.sign.name,
                        f"{pos.sign_degree:.6f}"
                    ])
            
            current += delta
    
    return str(output.absolute())


def export_ephemeris_json(
    start: datetime,
    end: datetime,
    planets: List[Planet],
    output_path: str,
    interval_days: float = 1.0,
    get_positions_callback = None
) -> str:
    """
    Export ephemeris data to JSON format.
    
    Args:
        start: Start date/time
        end: End date/time
        planets: List of planets to include
        output_path: Path to output JSON file
        interval_days: Time interval in days (default 1.0 = daily)
        get_positions_callback: Function(datetime, planet) -> PlanetPosition
                                Must be provided to get positions
    
    Returns:
        Path to created JSON file
    
    JSON Format:
        {
            "start": "2024-01-01T00:00:00",
            "end": "2024-12-31T23:59:59",
            "interval_days": 1.0,
            "data": [
                {
                    "timestamp": "2024-01-01T00:00:00",
                    "planets": {
                        "SUN": {
                            "longitude": 280.12,
                            "latitude": 0.00,
                            "speed_long": 1.02,
                            ...
                        }
                    }
                }
            ]
        }
    """
    if get_positions_callback is None:
        raise ValueError("get_positions_callback must be provided")
    
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    
    data = []
    current = start
    delta = timedelta(days=interval_days)
    
    while current <= end:
        entry = {
            "timestamp": current.isoformat(),
            "planets": {}
        }
        
        for planet in planets:
            pos = get_positions_callback(current, planet)
            if pos:
                entry["planets"][planet.name] = {
                    "longitude": pos.longitude,
                    "latitude": pos.latitude,
                    "speed_long": pos.speed_long,
                    "speed_lat": pos.speed_lat,
                    "speed_dist": pos.speed_dist,
                    "sign": pos.sign.name,
                    "sign_degree": pos.sign_degree,
                    "is_retrograde": pos.is_retrograde
                }
        
        data.append(entry)
        current += delta
    
    result = {
        "start": start.isoformat(),
        "end": end.isoformat(),
        "interval_days": interval_days,
        "planets": [p.name for p in planets],
        "data": data
    }
    
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    
    return str(output.absolute())
