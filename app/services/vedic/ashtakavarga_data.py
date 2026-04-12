from app.core.constants import Planet

# Ashtakavarga points relative to Natal positions.
# Format: planet_whose_ashtakavarga_is_calculated: {
#    planet_from_which_we_count: [relative_houses_that_get_a_point]
# }
# Planets: SUN=0, MOON=1, MARS=4, MERCURY=2, JUPITER=5, VENUS=3, SATURN=6
# Special key: "ASC" for Ascendant

ASHTAKAVARGA_POINTS = {
    Planet.SUN: {
        Planet.SUN: [1, 2, 4, 7, 8, 9, 10, 11],
        Planet.MOON: [3, 6, 10, 11],
        Planet.MARS: [1, 2, 4, 7, 8, 9, 10, 11],
        Planet.MERCURY: [3, 5, 6, 9, 10, 11, 12],
        Planet.JUPITER: [5, 6, 9, 11],
        Planet.VENUS: [6, 7, 12],
        Planet.SATURN: [1, 2, 4, 7, 8, 9, 10, 11],
        "ASC": [3, 4, 6, 10, 11, 12]
    },
    Planet.MOON: {
        Planet.SUN: [3, 6, 7, 8, 10, 11],
        Planet.MOON: [1, 3, 6, 7, 10, 11],
        Planet.MARS: [2, 3, 5, 6, 9, 10, 11],
        Planet.MERCURY: [1, 3, 4, 5, 7, 10, 11],
        Planet.JUPITER: [1, 4, 7, 8, 10, 11, 12],
        Planet.VENUS: [3, 4, 5, 7, 9, 10, 11],
        Planet.SATURN: [3, 5, 6, 11],
        "ASC": [3, 6, 10, 11]
    },
    Planet.MARS: {
        Planet.SUN: [3, 5, 6, 10, 11],
        Planet.MOON: [3, 6, 11],
        Planet.MARS: [1, 2, 4, 7, 8, 10, 11],
        Planet.MERCURY: [3, 5, 6, 11],
        Planet.JUPITER: [6, 10, 11, 12],
        Planet.VENUS: [6, 8, 11, 12],
        Planet.SATURN: [1, 4, 7, 8, 9, 10, 11],
        "ASC": [1, 3, 6, 10, 11]
    },
    Planet.MERCURY: {
        Planet.SUN: [5, 6, 9, 11, 12],
        Planet.MOON: [2, 4, 6, 8, 10, 11],
        Planet.MARS: [1, 2, 4, 7, 8, 9, 10, 11],
        Planet.MERCURY: [1, 3, 5, 6, 9, 10, 11, 12],
        Planet.JUPITER: [6, 8, 11, 12],
        Planet.VENUS: [1, 2, 3, 4, 5, 8, 9, 11],
        Planet.SATURN: [1, 2, 4, 7, 8, 9, 10, 11],
        "ASC": [1, 2, 4, 6, 8, 10, 11]
    },
    Planet.JUPITER: {
        Planet.SUN: [1, 2, 3, 4, 7, 8, 9, 10, 11],
        Planet.MOON: [2, 5, 7, 9, 11],
        Planet.MARS: [1, 2, 4, 7, 8, 10, 11],
        Planet.MERCURY: [1, 2, 4, 5, 6, 9, 10, 11],
        Planet.JUPITER: [1, 2, 3, 4, 7, 8, 10, 11],
        Planet.VENUS: [2, 5, 6, 9, 10, 11],
        Planet.SATURN: [3, 5, 6, 12],
        "ASC": [1, 2, 4, 5, 6, 7, 9, 10, 11]
    },
    Planet.VENUS: {
        Planet.SUN: [8, 11, 12],
        Planet.MOON: [1, 2, 3, 4, 5, 8, 9, 11, 12],
        Planet.MARS: [3, 5, 6, 9, 11, 12],
        Planet.MERCURY: [3, 5, 6, 9, 11],
        Planet.JUPITER: [5, 8, 9, 10, 11],
        Planet.VENUS: [1, 2, 3, 4, 5, 8, 9, 10, 11],
        Planet.SATURN: [3, 4, 5, 8, 9, 10, 11],
        "ASC": [1, 2, 3, 4, 5, 8, 9, 11]
    },
    Planet.SATURN: {
        Planet.SUN: [1, 2, 4, 7, 8, 10, 11],
        Planet.MOON: [3, 6, 11],
        Planet.MARS: [3, 5, 6, 10, 11, 12],
        Planet.MERCURY: [6, 8, 9, 10, 11, 12],
        Planet.JUPITER: [5, 6, 11, 12],
        Planet.VENUS: [6, 11, 12],
        Planet.SATURN: [3, 5, 6, 11],
        "ASC": [1, 3, 4, 6, 10, 11]
    }
}
