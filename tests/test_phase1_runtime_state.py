from datetime import UTC, datetime

from app.core.constants import Planet, SiderealMode
from app.core.ephemeris import Ephemeris
from app.core.ephemeris_context import EphemerisContext
from app.core.time import Time
from app.services.event_service import EventService
from app.services.metadata import get_engine_metadata


def test_ephemeris_context_restores_nested_sidereal_mode() -> None:
    ephemeris = Ephemeris()
    ephemeris.set_sidereal_mode(SiderealMode.LAHIRI)

    with EphemerisContext(sid_mode=SiderealMode.KRISHNAMURTI):
        assert ephemeris.sidereal_mode == SiderealMode.KRISHNAMURTI
        with EphemerisContext(sid_mode=SiderealMode.FAGAN_BRADLEY):
            assert ephemeris.sidereal_mode == SiderealMode.FAGAN_BRADLEY
        assert ephemeris.sidereal_mode == SiderealMode.KRISHNAMURTI

    assert ephemeris.sidereal_mode == SiderealMode.LAHIRI


def test_ephemeris_context_restores_topocentric_state() -> None:
    ephemeris = Ephemeris()
    ephemeris.reset_topocentric()

    with EphemerisContext(topo=(77.59, 12.97, 920.0)):
        assert ephemeris.topocentric == (77.59, 12.97, 920.0)

    assert ephemeris.topocentric == (0.0, 0.0, 0.0)


def test_tropical_calculation_isolated_from_prior_sidereal_state() -> None:
    ephemeris = Ephemeris()
    time = Time(datetime(2024, 3, 20, 3, 6, tzinfo=UTC))

    ephemeris.set_sidereal_mode(SiderealMode.KRISHNAMURTI)
    tropical_after_kp = ephemeris.calculate_planet(
        time.julian_day, Planet.SUN, sidereal=False, heliocentric=False
    )

    ephemeris.set_sidereal_mode(SiderealMode.LAHIRI)
    tropical_after_lahiri = ephemeris.calculate_planet(
        time.julian_day, Planet.SUN, sidereal=False, heliocentric=False
    )

    assert tropical_after_kp["longitude"] == tropical_after_lahiri["longitude"]
    assert tropical_after_kp["latitude"] == tropical_after_lahiri["latitude"]


def test_sidereal_modes_produce_distinct_longitudes() -> None:
    ephemeris = Ephemeris()
    time = Time(datetime(2024, 3, 20, 3, 6, tzinfo=UTC))

    ephemeris.set_sidereal_mode(SiderealMode.LAHIRI)
    lahiri = ephemeris.calculate_planet(time.julian_day, Planet.SUN, sidereal=True)
    ephemeris.set_sidereal_mode(SiderealMode.KRISHNAMURTI)
    krishnamurti = ephemeris.calculate_planet(time.julian_day, Planet.SUN, sidereal=True)

    assert lahiri["longitude"] != krishnamurti["longitude"]


def test_engine_metadata_reads_through_runtime_boundary() -> None:
    metadata = get_engine_metadata()

    assert metadata["sidereal_default"] == SiderealMode.LAHIRI.name
    assert "sidereal_mode" in metadata
    assert "topocentric" in metadata


def test_event_service_rise_set_restores_topocentric_state() -> None:
    ephemeris = Ephemeris()
    ephemeris.reset_topocentric()
    service = EventService(ephemeris)

    service.get_rise_set(
        Planet.SUN,
        Time(datetime(2024, 3, 20, 0, 0, tzinfo=UTC)),
        lat=51.5074,
        lon=-0.1278,
        alt=35.0,
    )

    assert ephemeris.topocentric == (0.0, 0.0, 0.0)
