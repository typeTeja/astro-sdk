from datetime import datetime, time as dt_time
from ...contexts import CalculationContext
from ...core.constants import Planet, SiderealMode
from ...core.ephemeris import Ephemeris
from ...core.ephemeris_context import EphemerisContext
from ...core.time import Time
from ...domain.vedic.panchanga import PanchangaData
from ...domain.common.metadata import DomainMetadata


class VedicPanchangaService:
    """
    Native 2.0 service for calculating the five elements (Panchanga) of Vedic time.
    Uses CalculationContext for explicit determinism.
    """

    TITHI_NAMES = [
        "Prathama", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashti", 
        "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi", 
        "Trayodashi", "Chaturdashi", "Purnima", "Prathama", "Dwitiya", 
        "Tritiya", "Chaturthi", "Panchami", "Shashti", "Saptami", "Ashtami", 
        "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", 
        "Chaturdashi", "Amavasya"
    ]

    NAKSHATRA_NAMES = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", 
        "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", 
        "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", 
        "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", 
        "Uttara Bhadrapada", "Revati"
    ]

    YOGA_NAMES = [
        "Vishkumbha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", 
        "Sukarma", "Dhriti", "Shula", "Ganda", "Vriddhi", "Dhruva", "Vyaghata", 
        "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyan", "Parigha", 
        "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", 
        "Vaidhriti"
    ]

    KARANA_NAMES = [
        "Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti", 
        "Shakuni", "Chatushpada", "Naga", "Kinstughna"
    ]

    VARA_NAMES = [
        "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
    ]

    def __init__(self, context: CalculationContext, ephemeris: Ephemeris | None = None) -> None:
        self.context = context
        self._eph = ephemeris or Ephemeris()

    def calculate_panchanga(
        self,
        time: Time,
        lat: float,
        lon: float,
        alt: float = 0.0
    ) -> PanchangaData:
        """
        Calculate Panchanga for a given time and location using the 2.0 context model.
        """
        z_ctx = self.context.zodiac
        sid_mode = z_ctx.sidereal_mode or SiderealMode.LAHIRI
        
        with EphemerisContext(sid_mode=sid_mode):
            # 1. Get Sun and Moon Positions (Sidereal)
            sun_pos = self._eph.calculate_planet(time.julian_day, Planet.SUN, sidereal=True)
            moon_pos = self._eph.calculate_planet(time.julian_day, Planet.MOON, sidereal=True)

            sun_lon = sun_pos["longitude"]
            moon_lon = moon_pos["longitude"]

            # 2. Tithi (12 degrees per Tithi)
            diff = (moon_lon - sun_lon) % 360
            tithi_idx = int(diff / 12)
            tithi_name = self.TITHI_NAMES[tithi_idx % 30]

            # 3. Nakshatra (13°20' per Nakshatra)
            nak_idx = int(moon_lon / (360 / 27))
            nak_name = self.NAKSHATRA_NAMES[nak_idx % 27]

            # 4. Yoga (Sun + Moon lon)
            yoga_idx = int((sun_lon + moon_lon) % 360 / (360 / 27))
            yoga_name = self.YOGA_NAMES[yoga_idx % 27]

            # 5. Karana (Half of Tithi, 6 degrees)
            karana_idx = int(diff / 6)
            karana_name = self.KARANA_NAMES[karana_idx % 11]

            # 6. Vara (Day of the week)
            vara_idx = (time.dt.weekday() + 1) % 7
            vara_name = self.VARA_NAMES[vara_idx]

            # 7. Sunrise/Sunset (Scope with topocentric context)
            with EphemerisContext(topo=(lon, lat, alt)):
                jd_start = Time(
                    datetime.combine(time.dt.date(), dt_time.min).replace(tzinfo=time.dt.tzinfo)
                ).julian_day
                rise_jd = self._eph.calculate_rise_set(jd_start, Planet.SUN, lat, lon, alt, is_rise=True)
                set_jd = self._eph.calculate_rise_set(jd_start, Planet.SUN, lat, lon, alt, is_rise=False)

            return PanchangaData(
                tithi=tithi_name,
                vara=vara_name,
                nakshatra=nak_name,
                yoga=yoga_name,
                karana=karana_name,
                sunrise=Time.from_julian_day(rise_jd).dt if rise_jd else time.dt,
                sunset=Time.from_julian_day(set_jd).dt if set_jd else time.dt,
                metadata=DomainMetadata(
                    capability="vedic.panchanga",
                    maturity=self.context.feature.maturity.value,
                    fingerprint=self.context.fingerprint
                )
            )
