from typing import Any, Self

from app.core.constants import SiderealMode
from app.core.ephemeris import _SWISS_LOCK, Ephemeris


class EphemerisContext:
    """
    Context manager to isolate Swiss Ephemeris global state.
    Ensures that temporary changes to sidereal mode, topocentric positions,
    or tidal acceleration are restored after the context exits.
    """

    def __init__(
        self,
        sid_mode: SiderealMode | None = None,
        topo: tuple[float, float, float] | None = None,
        tidal: float | None = None,
    ) -> None:
        self.sid_mode = sid_mode
        self.topo = topo
        self.tidal = tidal

        self._prev_sid_mode: SiderealMode | None = None
        self._prev_topo: tuple[float, float, float] | None = None
        self._prev_tidal: float | str | None = None

    def __enter__(self) -> Self:
        with _SWISS_LOCK:
            ephemeris = Ephemeris()
            if self.sid_mode is not None:
                self._prev_sid_mode = ephemeris.sidereal_mode
                ephemeris.set_sidereal_mode(self.sid_mode, 0, 0)

            if self.topo is not None:
                self._prev_topo = ephemeris.topocentric
                ephemeris.set_topocentric(self.topo[1], self.topo[0], self.topo[2])

            if self.tidal is not None:
                self._prev_tidal = ephemeris.tidal_acceleration
                ephemeris.set_tidal_acceleration(self.tidal)

            return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        with _SWISS_LOCK:
            ephemeris = Ephemeris()
            # Restore tidal acceleration to automatic
            if self.tidal is not None:
                if isinstance(self._prev_tidal, float):
                    ephemeris.set_tidal_acceleration(self._prev_tidal)
                else:
                    ephemeris.reset_tidal_acceleration()

            # Restore the actual previous sidereal mode (not always Lahiri)
            if self.sid_mode is not None:
                restore = self._prev_sid_mode if self._prev_sid_mode is not None else SiderealMode.LAHIRI
                ephemeris.set_sidereal_mode(restore, 0, 0)

            # Reset topocentric parameters to geocentric center
            if self.topo is not None:
                if self._prev_topo is not None:
                    ephemeris.set_topocentric(
                        self._prev_topo[1], self._prev_topo[0], self._prev_topo[2]
                    )
                else:
                    ephemeris.reset_topocentric()
