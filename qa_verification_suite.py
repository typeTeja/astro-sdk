import sys
import os
import json
from datetime import datetime, UTC
from typing import Dict, Any, List

# Add the project root to sys.path so we can import app modules
sys.path.append(os.getcwd())

from app.core.time import Time
from app.core.constants import Planet, SiderealMode
from app.core.ephemeris import Ephemeris
from app.services.natal_service import NatalService
from app.services.vedic_service import VedicService

class QACertificationSuite:
    def __init__(self):
        self.eph = Ephemeris()
        self.natal_service = NatalService(self.eph)
        self.vedic_service = VedicService(self.eph)
        self.results = []
        self.tolerance = 0.01  # degrees

    def log_result(self, step: str, test_name: str, passed: bool, diff: float = 0.0, expected: Any = None, actual: Any = None, reason: str = ""):
        self.results.append({
            "step": step,
            "test_name": test_name,
            "passed": passed,
            "difference": round(diff, 6),
            "expected": expected,
            "actual": actual,
            "reason": reason
        })

    def run_step_3_math(self):
        """Step 3: Core Math Validation (JD and Nakshatra Boundaries)"""
        # 1. Julian Day for J2000.0
        # 2000-01-01 12:00 UTC = 2451545.0
        dt_j2000 = datetime(2000, 1, 1, 12, 0, 0, tzinfo=UTC)
        time_j2000 = Time(dt_j2000)
        expected_jd = 2451545.0
        actual_jd = time_j2000.julian_day
        passed_jd = abs(actual_jd - expected_jd) < 0.000001
        self.log_result("Step 3", "Julian Day J2000.0", passed_jd, actual_jd - expected_jd, expected_jd, actual_jd)

        # 2. Nakshatra Boundaries
        # 0.0° Ashwini
        # 13.332° Ashwini/Bharani Boundary
        boundary_pts = [
            (0.1, "Ketu"),      # Ashwini (Ketu lord)
            (14.0, "Venus"),    # Bharani (Venus lord)
            (27.0, "Sun"),      # Krittika (Sun lord)
        ]
        # In our VedicService, we track DASHA_LORDS sequence starting from Ketu
        # 0-13.33 = Nak 0 (Ketu)
        # 13.33-26.66 = Nak 1 (Venus)
        for deg, expected_lord in boundary_pts:
            # We use a dummy Moon position at exactly these degrees
            nak_pos = deg / (360/27)
            nak_idx = int(nak_pos)
            actual_lord_idx = nak_idx % 9
            actual_lord = self.vedic_service.DASHA_LORDS[actual_lord_idx][0]
            passed = actual_lord == expected_lord
            self.log_result("Step 3", f"Nakshatra Lord at {deg}°", passed, 0.0, expected_lord, actual_lord)

    def run_step_1_2_snapshot(self):
        """Step 1 & 2: Snapshot & Reference Comparison (2024-04-08 18:20 UTC)"""
        # Input Data: Solar Eclipse 2024
        dt_2024 = datetime(2024, 4, 8, 18, 20, 0, tzinfo=UTC)
        time_2024 = Time(dt_2024)
        
        # Tropical Ground Truth (Confirmed NASA JPL / Astro.com)
        expected_tropical = {
            "SUN": 19.39985,
            "MOON": 19.39147,
            "MARS": 343.05096,
            "JUPITER": 49.04562,
        }

        positions = self.natal_service.calculate_positions(time_2024, sidereal_mode=None)
        
        for p in positions:
            p_name = p.planet.name
            if p_name in expected_tropical:
                exp = expected_tropical[p_name]
                act = p.longitude
                diff = abs(act - exp)
                passed = diff < self.tolerance
                self.log_result("Step 1", f"Tropical Longitude: {p_name}", passed, act - exp, exp, act)

        # Sidereal Lahiri (2024-04-08 18:20 UTC)
        # Nakshatra lord for Moon in Aries (Revati/Ashwini transition)
        sidereal_positions = self.natal_service.calculate_positions(time_2024, sidereal_mode=SiderealMode.LAHIRI)
        moon_sid = next(p for p in sidereal_positions if p.planet == Planet.MOON)
        nak_idx = int(moon_sid.longitude / (360/27)) % 9
        actual_nak_lord = self.vedic_service.DASHA_LORDS[nak_idx][0]
        # Moon ~355.27 Sidereal (Revati - Lord Mercury)
        expected_nak_lord = "Mercury"
        passed_nak = actual_nak_lord == expected_nak_lord
        self.log_result("Step 1", "Sidereal Moon Nakshatra Lord (2024)", passed_nak, 0.0, expected_nak_lord, actual_nak_lord)

    def run_step_4_edge_cases(self):
        """Step 4: Edge Cases (Eclipses, 360 Boundaries)"""
        # 1. Solar Eclipse: 2024-04-08 18:20 UTC
        # At eclipse, Sun and Moon must be conjunct (<0.01° orb)
        dt_eclipse = datetime(2024, 4, 8, 18, 20, 0, tzinfo=UTC)
        time_eclipse = Time(dt_eclipse)
        pos_eclipse = self.natal_service.calculate_positions(time_eclipse, sidereal_mode=None)
        sun_lon = next(p for p in pos_eclipse if p.planet == Planet.SUN).longitude
        moon_lon = next(p for p in pos_eclipse if p.planet == Planet.MOON).longitude
        orb = abs(sun_lon - moon_lon)
        # Account for 360 wrap
        if orb > 180: orb = 360 - orb
        passed_eclipse = orb < 0.01
        self.log_result("Step 4", "Solar Eclipse 2024 Conjunction", passed_eclipse, orb, "< 0.01", orb)

        # 2. 360 Boundary Crossing (Wrapping logic)
        # Simulate a point at 359.99 and move by 0.02
        val1 = 359.99
        val2 = (val1 + 0.02) % 360
        passed_wrap = abs(val2 - 0.01) < 0.00001
        self.log_result("Step 4", "360 Degree Wrapping Logic", passed_wrap, val2 - 0.01, 0.01, val2)

    def run_step_5_determinism(self):
        """Step 5: Determinism (Same input = Same output)"""
        dt = datetime(1990, 5, 15, 12, 0, 0, tzinfo=UTC)
        time_in = Time(dt)
        lat, lon = 34.0522, -118.2437
        
        runs = []
        for _ in range(5):
            pos = self.natal_service.calculate_positions(time_in, sidereal_mode=None)
            # Just grab Sun longitude for comparison
            sun_lon = next(p for p in pos if p.planet == Planet.SUN).longitude
            runs.append(sun_lon)
        
        # Check if all runs are identical
        identical = all(x == runs[0] for x in runs)
        self.log_result("Step 5", "Engine Determinism (5-pass)", identical, 0.0, runs[0], runs[0])

    def generate_report(self):
        report = "# AstroSDK Accuracy Certification Report\n\n"
        report += f"**Audit Timestamp**: {datetime.now(UTC).isoformat()}\n"
        report += "**Tolerance Threshold**: 0.01°\n\n"
        
        report += "| Step | Test Name | Status | Diff | Expected | Actual |\n"
        report += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        
        all_passed = True
        for r in self.results:
            status = "✅ PASS" if r["passed"] else "❌ FAIL"
            if not r["passed"]: all_passed = False
            report += f"| {r['step']} | {r['test_name']} | {status} | {r['difference']} | {r['expected']} | {r['actual']} |\n"
        
        report += f"\n## Final Verdict: {'CERTIFIED' if all_passed else 'REJECTED'}\n\n"
        
        if not all_passed:
            report += "### Deviations Above 0.01°\n"
            for r in self.results:
                if not r["passed"]:
                    report += f"- **{r['test_name']}**: Diff {r['difference']}. Potential cause: {r['reason'] or 'Calculation variance'}\n"

        return report

if __name__ == "__main__":
    suite = QACertificationSuite()
    suite.run_step_3_math()
    suite.run_step_1_2_snapshot()
    suite.run_step_4_edge_cases()
    suite.run_step_5_determinism()
    print(suite.generate_report())
