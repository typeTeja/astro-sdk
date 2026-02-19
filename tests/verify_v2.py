from astrosdk import create_sdk, Time
from datetime import datetime

def verify_v2():
    print("1. Initializing SDK...")
    sdk = create_sdk()
    print("   SDK Initialized.")
    
    print("2. Creating Time...")
    t = Time(datetime.now().astimezone())
    print(f"   Time: {t}")
    print(f"   Julian Day: {t.julian_day}")
    
    print("3. Calculating Natal Chart...")
    chart = sdk.create_natal_chart(
        time=t,
        latitude=40.7128,
        longitude=-74.0060
    )
    print("   Chart Calculated.")
    
    print("4. Inspecting Planets...")
    for p in chart.planets:
        print(f"   {p.planet.name}: {p.longitude:.2f} deg in {p.sign.name}")
        
    print("5. Inspecting Houses...")
    for h in chart.houses.cusps:
        print(f"   House {h.number}: {h.longitude:.2f}")

if __name__ == "__main__":
    verify_v2()
