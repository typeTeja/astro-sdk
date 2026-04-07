from ..domain.aspect import Aspect
from ..domain.planet import PlanetPosition


class AspectService:
    """
    Calculates aspects between planets.
    """

    # Major Aspects (Ptolemaic)
    MAJOR_ASPECTS = {
        0.0: "CONJUNCTION",
        60.0: "SEXTILE",
        90.0: "SQUARE",
        120.0: "TRINE",
        180.0: "OPPOSITION",
    }

    # Minor Aspects
    MINOR_ASPECTS = {
        30.0: "SEMI-SEXTILE",
        45.0: "SEMI-SQUARE",
        135.0: "SESQUI-QUADRATE",
        150.0: "QUINCUNX",
    }

    # Kepler Aspects (Quintile family)
    KEPLER_ASPECTS = {72.0: "QUINTILE", 144.0: "BIQUINTILE"}

    # Septile family (7th harmonic)
    SEPTILE_ASPECTS = {
        360 / 7: "SEPTILE",    # 51.42857...°
        720 / 7: "BISEPTILE",  # 102.85714...°
        1080 / 7: "TRISEPTILE",  # 154.28571...°
    }

    # Novile family (9th harmonic)
    NOVILE_ASPECTS = {
        40.0: "NOVILE",  # 360/9
        80.0: "BINOVILE",  # 720/9
        160.0: "QUADNOVILE",  # 1440/9
    }

    # Undecile family (11th harmonic)
    UNDECILE_ASPECTS = {
        360 / 11: "UNDECILE",    # 32.72727...°
        720 / 11: "BIUNDECILE",  # 65.45454...°
        1080 / 11: "TRIUNDECILE",  # 98.18181...°
    }

    # All aspects combined
    ASPECT_ANGLES = {
        **MAJOR_ASPECTS,
        **MINOR_ASPECTS,
        **KEPLER_ASPECTS,
        **SEPTILE_ASPECTS,
        **NOVILE_ASPECTS,
        **UNDECILE_ASPECTS,
    }

    # Default orbs for each aspect type
    DEFAULT_ORBS = {
        # Major aspects (wider orbs)
        "CONJUNCTION": 10.0,
        "SEXTILE": 6.0,
        "SQUARE": 8.0,
        "TRINE": 8.0,
        "OPPOSITION": 10.0,
        # Minor aspects (medium orbs)
        "SEMI-SEXTILE": 3.0,
        "SEMI-SQUARE": 3.0,
        "SESQUI-QUADRATE": 3.0,
        "QUINCUNX": 3.0,
        # Kepler aspects (medium orbs)
        "QUINTILE": 2.0,
        "BIQUINTILE": 2.0,
        # Septile family (tight orbs)
        "SEPTILE": 1.5,
        "BISEPTILE": 1.5,
        "TRISEPTILE": 1.5,
        # Novile family (tight orbs)
        "NOVILE": 1.5,
        "BINOVILE": 1.5,
        "QUADNOVILE": 1.5,
        # Undecile family (tight orbs)
        "UNDECILE": 1.0,
        "BIUNDECILE": 1.0,
        "TRIUNDECILE": 1.0,
    }

    def calculate_aspects(
        self,
        planets: list[PlanetPosition],
        aspect_types: list[str] | None = None,
        custom_orbs: dict[str, float] | None = None,
        global_orb: float | None = None,
    ) -> list[Aspect]:
        """
        Calculate aspects between planets.

        Args:
            planets: List of planet positions
            aspect_types: Optional list of aspect type filters:
                         'major', 'minor', 'kepler', 'septile', 'novile', 'undecile', 'all'
                         Default is ['major'] for backward compatibility
            custom_orbs: Optional dict of custom orbs to override defaults per aspect
            global_orb: Optional global orb fallback for all aspects

        Returns:
            List of aspects found
        """
        if aspect_types is None:
            aspect_types = ["major"]  # Default to major aspects only

        # Build the aspect angles to check based on requested types
        angles_to_check: dict[float, str] = {}
        if "all" in aspect_types:
            angles_to_check = self.ASPECT_ANGLES
        else:
            if "major" in aspect_types:
                angles_to_check.update(self.MAJOR_ASPECTS)
            if "minor" in aspect_types:
                angles_to_check.update(self.MINOR_ASPECTS)
            if "kepler" in aspect_types:
                angles_to_check.update(self.KEPLER_ASPECTS)
            if "septile" in aspect_types:
                angles_to_check.update(self.SEPTILE_ASPECTS)
            if "novile" in aspect_types:
                angles_to_check.update(self.NOVILE_ASPECTS)
            if "undecile" in aspect_types:
                angles_to_check.update(self.UNDECILE_ASPECTS)

        # Merge custom orbs with defaults, following priority
        orbs = self.DEFAULT_ORBS.copy()

        if global_orb is not None:
            # Overwrite all defaults with global fallback
            for aspect_name in orbs:
                orbs[aspect_name] = global_orb

        if custom_orbs:
            # Final priority: specific overrides
            orbs.update(custom_orbs)

        results = []
        for i, p1 in enumerate(planets):
            for p2 in planets[i + 1 :]:
                aspect = self.get_aspect(p1, p2, angles_to_check, orbs)
                if aspect:
                    results.append(aspect)
        return results

    def get_aspect(
        self,
        p1: PlanetPosition,
        p2: PlanetPosition,
        angles_to_check: dict[float, str] | None = None,
        orbs: dict[str, float] | None = None,
    ) -> Aspect | None:
        """
        Get aspect between two planet positions.

        Args:
            p1: First planet position
            p2: Second planet position
            angles_to_check: Dict of angles to check (defaults to all aspects)
            orbs: Dict of orbs to use (defaults to DEFAULT_ORBS)

        Returns:
            Aspect if found within orb, None otherwise
        """
        if angles_to_check is None:
            angles_to_check = self.ASPECT_ANGLES
        if orbs is None:
            orbs = self.DEFAULT_ORBS

        diff = abs(p1.longitude - p2.longitude)
        if diff > 180:
            diff = 360 - diff

        for angle, name in angles_to_check.items():
            orb_limit = orbs.get(name, 0.0)
            actual_orb = abs(diff - angle)

            if actual_orb <= orb_limit:
                # Determine applying/separating based on relative velocity
                # An aspect is "applying" if the planets are moving closer to exactitude
                # Normalize the angular difference to -180 to 180
                angular_diff = (p2.longitude - p1.longitude + 180) % 360 - 180

                # Relative speed (how fast p2 is moving relative to p1)
                relative_speed = p2.speed_long - p1.speed_long

                # For conjunction (angle 0)
                if angle == 0.0:
                    is_applying = (angular_diff > 0 and relative_speed < 0) or (
                        angular_diff < 0 and relative_speed > 0
                    )
                elif angle == 180.0:  # Opposition
                    if angular_diff > 0:
                        is_applying = relative_speed < 0 and angular_diff < 180
                    else:
                        is_applying = relative_speed > 0 and angular_diff > -180
                else:  # Other aspects (60, 90, 120)
                    is_applying = relative_speed < 0 if angular_diff > 0 else relative_speed > 0

                return Aspect(
                    p1=p1.planet,
                    p2=p2.planet,
                    angle=diff,
                    orb=actual_orb,
                    type=name,
                    applying=is_applying,
                )
        return None
