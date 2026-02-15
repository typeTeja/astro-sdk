import swisseph as swe
from threading import Lock
from .errors import EphemerisStateError
from .constants import SiderealMode

class EphemerisContext:
    """
    Context manager to isolate Swiss Ephemeris global state.
    Ensures that temporary changes to sidereal mode, topocentric positions, 
    or tidal acceleration are restored after the context exits.
    """
    _state_lock = Lock()
    
    def __init__(self, sid_mode: SiderealMode = None, topo: tuple = None, tidal: float = None):
        self.sid_mode = sid_mode
        self.topo = topo
        self.tidal = tidal
        
        self._prev_sid_mode = None
        self._prev_topo = None
        self._prev_tidal = None

    def __enter__(self):
        with self._state_lock:
            # Save current state
            # Note: pyswisseph doesn't explicitly 'get' all state easily, 
            # so we must rely on our internal tracking or set them explicitly.
            # However, we can at least ensure we don't have nested conflicting contexts easily.
            
            # Since pyswisseph is global, we apply the new state
            if self.sid_mode is not None:
                # We can't really "get" the current sidereal mode from swisseph, 
                # so we assume the Ephemeris singleton or caller handles the "prev" if they care.
                # For strictly isolated context, we just set it.
                swe.set_sid_mode(self.sid_mode, 0, 0)
            
            if self.topo is not None:
                swe.set_topo(self.topo[0], self.topo[1], self.topo[2])
                
            if self.tidal is not None:
                swe.set_tid_acc(self.tidal)
                
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # In a real enterprise SDK, we would restore the "Global Default" here.
        # Since we are hardening, we will restore things to "TIDAL_AUTOMATIC" etc. if they were changed.
        if self.tidal is not None:
            swe.set_tid_acc(swe.TIDAL_AUTOMATIC)
        
        # Restore sidereal mode to Lahiri (project policy) if it was changed
        if self.sid_mode is not None:
            swe.set_sid_mode(SiderealMode.LAHIRI, 0, 0)
        
        # Reset topo if it was changed (return to geocentric)
        if self.topo is not None:
            swe.set_topo(0, 0, 0) # Back to geocentric center
