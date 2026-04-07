from threading import Lock
from typing import Any, Self

import swisseph as swe

from .constants import SiderealMode


class EphemerisContext:
    """
    Context manager to isolate Swiss Ephemeris global state.
    Ensures that temporary changes to sidereal mode, topocentric positions,
    or tidal acceleration are restored after the context exits.
    """

    _state_lock = Lock()

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
        self._prev_tidal: float | None = None

    def __enter__(self) -> Self:
        with self._state_lock:
            if self.sid_mode is not None:
                # Save the actual current sidereal mode before overwriting
                try:
                    prev_mode_id = int(swe.get_ayanamsa_ex_ut(0, 0)[0])  # type: ignore[attr-defined]
                    self._prev_sid_mode = SiderealMode(prev_mode_id)
                except Exception:
                    # Fallback to project default if we cannot determine current mode
                    self._prev_sid_mode = SiderealMode.LAHIRI
                swe.set_sid_mode(self.sid_mode, 0, 0)

            if self.topo is not None:
                swe.set_topo(self.topo[0], self.topo[1], self.topo[2])

            if self.tidal is not None:
                swe.set_tid_acc(self.tidal)

            return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        with self._state_lock:
            # Restore tidal acceleration to automatic
            if self.tidal is not None:
                swe.set_tid_acc(swe.TIDAL_AUTOMATIC)

            # Restore the actual previous sidereal mode (not always Lahiri)
            if self.sid_mode is not None:
                restore = self._prev_sid_mode if self._prev_sid_mode is not None else SiderealMode.LAHIRI
                swe.set_sid_mode(restore, 0, 0)

            # Reset topocentric parameters to geocentric center
            if self.topo is not None:
                swe.set_topo(0, 0, 0)
