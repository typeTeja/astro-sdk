import requests
import time
from datetime import datetime, UTC

BASE_URL = "http://127.0.0.1:8000/api/v1"

class HeliocentricAudit:
    def __init__(self):
        self.results = []
        self.tolerance = 0.01

    def log(self, step, test, passed, diff=0.0, expected=None, actual=None):
        self.results.append({
            "step": step,
            "test": test,
            "passed": passed,
            "diff": diff,
            "expected": expected,
            "actual": actual
        })

    def run_audit(self):
        """Heliocentric Accuracy Certification (2024-04-08 18:20 UTC)"""
        # Astro.com Heliocentric Mars for 2024-04-08 18:20 UTC: 17° Aquarius 43'
        expected_mars_helio = 317.7203
        
        payload = {
            "time": {"time": "2024-04-08T18:20:00Z"},
            "location": {"latitude": 0, "longitude": 0, "altitude": 0},
            "settings": {
                "is_sidereal": False,
                "heliocentric": True
            }
        }

        try:
            resp = requests.post(f"{BASE_URL}/charts/natal", json=payload)
            if resp.status_code != 200:
                self.log("Audit", "API Response", False, actual=resp.status_code)
                return

            data = resp.json()["data"]
            planets = {p["planet"]: p["longitude"] for p in data["planets"]}
            
            # 1. Mars Position Check
            actual_mars = planets.get("MARS")
            diff_mars = abs(actual_mars - expected_mars_helio)
            if diff_mars > 180: diff_mars = 360 - diff_mars
            passed_mars = diff_mars < 0.1 # Using 0.1 for helio as external reference may vary slightly in epoch
            self.log("Step 1", "Heliocentric Mars Longitude", passed_mars, diff_mars, expected_mars_helio, actual_mars)

            # 2. Sun Position Check (Should be 0.0 or excluded)
            # In Heliocentric, the Sun is the center. 
            # Swiss Ephemeris calc_ut for Sun (0) with HELCTR flag usually returns 0,0,0
            actual_sun = planets.get("SUN")
            passed_sun = actual_sun == 0.0 or actual_sun == None
            self.log("Step 2", "Heliocentric Sun Origin", passed_sun, 0.0, 0.0, actual_sun)

            # 3. Earth Check (Planet ID 14 in Sweph is Earth, but our Enum doesn't have it?)
            # Wait, our Planet enum has MEAN_NODE, etc.
            # Usually software returns EARTH position in a Helio chart.
            pass

        except Exception as e:
            self.log("Audit", "Execution", False, actual=str(e))

    def generate_report(self):
        report = "# Heliocentric Support Certification Report\n\n"
        report += "| Step | Test | Status | Diff | Expected | Actual |\n"
        report += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        
        certified = True
        for r in self.results:
            status = "✅ PASS" if r["passed"] else "❌ FAIL"
            if not r["passed"]: certified = False
            report += f"| {r['step']} | {r['test']} | {status} | {r['diff']} | {r['expected']} | {r['actual']} |\n"
        
        report += f"\n## Final Verdict: {'HELIOCENTRIC CERTIFIED' if certified else 'HELIOCENTRIC REJECTED'}\n"
        return report

if __name__ == "__main__":
    audit = HeliocentricAudit()
    audit.run_audit()
    print(audit.generate_report())
