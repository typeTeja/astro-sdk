# AstroData Verification Guide

Ensuring the accuracy of astronomical data is critical for professional research and financial modeling. AstroSDK is built on the **Swiss Ephemeris**, which is based on NASA's JPL DE431/DE432 planetary ephemerides—the global standard for high-precision calculations.

## 1. Ground Truth Cross-Verification
To verify AstroSDK data manually, you can compare specific API outputs against these industry-standard benchmarks:

### Trusted External Sources
*   **[NASA Horizons](https://ssd.jpl.nasa.gov/horizons/app.html)**: The absolute source of truth for planetary positions.
*   **[Astrodienst (Astro.com)](https://www.astro.com/swisseph/sweph_e.htm)**: A web interface for the same Swiss Ephemeris engine used by AstroSDK.
*   **[Swiss Ephemeris Official PDF Ephemerides](https://www.astro.com/swisseph/swepha_e.htm)**: Pre-calculated tables for verification.

### Manual Verification Procedure
1.  Choose a date/time (e.g., **2024-04-08 18:00:00 UTC**).
2.  Call the AstroSDK Geocentric endpoint:
    ```json
    {
      "time": { "time": "2024-04-08T18:00:00Z" },
      "location": { "latitude": 0, "longitude": 0, "altitude": 0 }
    }
    ```
3.  Compare the `longitude` of Sun/Moon against NASA Horizons for that specific Julian Day.

> [!NOTE] 
> **Standard vs. Sidereal Verification**: If comparing against standard astronomy sources, ensure you set `"is_sidereal": false` in your request. Standard astronomy uses Tropical coordinates (J2000).

---

## 2. Automated Regression Testing
AstroSDK includes a high-precision testing suite that validates the engine against mathematically certain events (Eclipses, Ingresses, Conversions).

### Run the Integrity Suite
Execute this in your terminal to verify the C-bindings and coordinate logic are working perfectly on your machine:
```bash
pytest tests/regression/ -v
```

### What these tests verify:
*   **Determinism**: Ensuring the same input always yields the exact same output.
*   **Geometric Bounds**: 0-360 wraparound logic.
*   **Event Accuracy**: Validating that historical solar eclipses and planetary returns match known astronomical records.

---

## 3. High-Precision Flags
For maximum precision (arc-second accuracy), ensure your payloads include:
1.  **Timezone Accuracy**: Always use `Z` or explicit offsets.
2.  **Delta-T Calculation**: AstroSDK automatically handles Delta-T corrections (the difference between atomic time and earth rotation time), ensuring precision even for dates thousands of years in the past/future.

---

### Verification Example Case (Lunar Phase)
*   **New Moon (Solar Eclipse)**: April 8, 2024.
*   **AstroSDK Logic**: At the exact moment of a solar eclipse, Sun and Moon longitude should be identical (Conjunction).
*   **Test**: Request Sun and Moon positions for `2024-04-08T18:20:00Z`. Their longitudes will match within 0.0001 degrees.
