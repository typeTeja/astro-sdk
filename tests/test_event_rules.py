"""
Tests for Custom Event Rule Engine
"""

import pytest
from datetime import datetime, timezone
from astrosdk.domain.event_rules import (
    AspectCondition,
    DignityCondition,
    CombustionCondition,
    SpeedCondition,
    RetrogradeCondition,
    LongitudeCondition,
    EventRule,
    LogicOperator,
    RuleMatch,
    evaluate_rule_at_time,
    scan_time_range
)
from astrosdk.domain.planet import PlanetPosition
from astrosdk.domain.aspect import Aspect
from astrosdk.domain.dignity import DignityType
from astrosdk.domain.combustion import CombustionState
from astrosdk.core.constants import Planet, ZodiacSign


# Helper to create simple planet position
def make_planet(planet, longitude, speed_long=0.5):
    return PlanetPosition(
        planet=planet,
        longitude=longitude,
        latitude=0.0,
        distance=1.0,
        speed_long=speed_long,
        speed_lat=0.0,
        speed_dist=0.0
    )


class TestAspectCondition:
    """Test aspect condition evaluation."""
    
    def test_aspect_found(self):
        """Aspect condition matches when aspect exists."""
        condition = AspectCondition(
            planet1=Planet.MOON,
            planet2=Planet.VENUS,
            aspect="trine"
        )
        
        aspects = [
            Aspect(
                p1=Planet.MOON,
                p2=Planet.VENUS,
                angle=120.0,
                orb=2.0,
                type="trine",
                applying=True
            )
        ]
        
        assert condition.evaluate(aspects) is True
    
    def test_aspect_not_found(self):
        """Aspect condition fails when aspect doesn't exist."""
        condition = AspectCondition(
            planet1=Planet.SUN,
            planet2=Planet.MARS,
            aspect="square"
        )
        
        aspects = [
            Aspect(
                p1=Planet.MOON,
                p2=Planet.VENUS,
                angle=120.0,
                orb=2.0,
                type="trine",
                applying=True
            )
        ]
        
        assert condition.evaluate(aspects) is False
    
    def test_aspect_reversed_planets(self):
        """Aspect condition matches regardless of planet order."""
        condition = AspectCondition(
            planet1=Planet.VENUS,
            planet2=Planet.MOON,
            aspect="trine"
        )
        
        aspects = [
            Aspect(
                p1=Planet.MOON,
                p2=Planet.VENUS,
                angle=120.0,
                orb=2.0,
                type="trine",
                applying=True
            )
        ]
        
        assert condition.evaluate(aspects) is True


class TestDignityCondition:
    """Test dignity condition evaluation."""
    
    def test_dignity_match(self):
        """Dignity condition matches when planet has dignity."""
        condition = DignityCondition(
            planet=Planet.VENUS,
            dignity=DignityType.EXALTATION
        )
        
        # Venus at 27° Pisces (exaltation)
        planets = [make_planet(Planet.VENUS, 357.0)]
        
        assert condition.evaluate(planets) is True


class TestCombustionCondition:
    """Test combustion condition evaluation."""
    
    def test_combust_detected(self):
        """Combustion condition detects combust planets."""
        condition = CombustionCondition(
            planet=Planet.MERCURY,
            state=CombustionState.COMBUST
        )
        
        planets = [
            make_planet(Planet.SUN, 100.0),
            make_planet(Planet.MERCURY, 105.0)  # 5° from Sun
        ]
        
        assert condition.evaluate(planets) is True


class TestSpeedCondition:
    """Test speed condition evaluation."""
    
    def test_speed_greater_than(self):
        """Speed condition with > operator."""
        condition = SpeedCondition(
            planet=Planet.MOON,
            operator=">",
            value=12.0
        )
        
        planets = [make_planet(Planet.MOON, 100.0, speed_long=13.5)]
        
        assert condition.evaluate(planets) is True
    
    def test_speed_less_than(self):
        """Speed condition with < operator."""
        condition = SpeedCondition(
            planet=Planet.SATURN,
            operator="<",
            value=0.1
        )
        
        planets = [make_planet(Planet.SATURN, 100.0, speed_long=0.05)]
        
        assert condition.evaluate(planets) is True


class TestRetrogradeCondition:
    """Test retrograde condition evaluation."""
    
    def test_is_retrograde(self):
        """Detects retrograde motion (negative speed)."""
        condition = RetrogradeCondition(
            planet=Planet.MERCURY,
            is_retrograde=True
        )
        
        planets = [make_planet(Planet.MERCURY, 100.0, speed_long=-1.2)]
        
        assert condition.evaluate(planets) is True
    
    def test_not_retrograde(self):
        """Detects direct motion."""
        condition = RetrogradeCondition(
            planet=Planet.JUPITER,
            is_retrograde=False
        )
        
        planets = [make_planet(Planet.JUPITER, 100.0, speed_long=0.2)]
        
        assert condition.evaluate(planets) is True


class TestLongitudeCondition:
    """Test longitude range condition evaluation."""
    
    def test_longitude_in_range(self):
        """Planet longitude within range."""
        condition = LongitudeCondition(
            planet=Planet.SUN,
            min_longitude=90.0,
            max_longitude=120.0
        )
        
        planets = [make_planet(Planet.SUN, 105.0, speed_long=1.0)]
        
        assert condition.evaluate(planets) is True
    
    def test_longitude_wraparound(self):
        """Longitude range wrapping around 0°."""
        condition = LongitudeCondition(
            planet=Planet.MARS,
            min_longitude=350.0,
            max_longitude=10.0
        )
        
        # Test 355° (should match)
        planets = [make_planet(Planet.MARS, 355.0)]
        assert condition.evaluate(planets) is True
        
        # Test 5° (should match)
        planets = [make_planet(Planet.MARS, 5.0)]
        assert condition.evaluate(planets) is True


class TestEventRule:
    """Test complete event rules with multiple conditions."""
    
    def test_rule_and_logic_all_match(self):
        """Rule with AND logic matches when all conditions true."""
        rule = EventRule(
            name="Test Rule",
            conditions=[
                SpeedCondition(planet=Planet.MOON, operator=">", value=12.0),
                LongitudeCondition(planet=Planet.SUN, min_longitude=0.0, max_longitude=30.0)
            ],
            logic=LogicOperator.AND
        )
        
        planets = [
            make_planet(Planet.MOON, 100.0, speed_long=13.0),
            make_planet(Planet.SUN, 15.0, speed_long=1.0)
        ]
        
        assert rule.evaluate(planets, []) is True
    
    def test_rule_and_logic_partial_match(self):
        """Rule with AND logic fails when any condition false."""
        rule = EventRule(
            name="Test Rule",
            conditions=[
                SpeedCondition(planet=Planet.MOON, operator=">", value=12.0),
                LongitudeCondition(planet=Planet.SUN, min_longitude=0.0, max_longitude=30.0)
            ],
            logic=LogicOperator.AND
        )
        
        planets = [
            make_planet(Planet.MOON, 100.0, speed_long=11.0),  # Fails
            make_planet(Planet.SUN, 15.0, speed_long=1.0)
        ]
        
        assert rule.evaluate(planets, []) is False
    
    def test_rule_or_logic(self):
        """Rule with OR logic matches when any condition true."""
        rule = EventRule(
            name="Test Rule",
            conditions=[
                SpeedCondition(planet=Planet.MOON, operator=">", value=12.0),
                LongitudeCondition(planet=Planet.SUN, min_longitude=0.0, max_longitude=30.0)
            ],
            logic=LogicOperator.OR
        )
        
        # Only second condition matches
        planets = [
            make_planet(Planet.MOON, 100.0, speed_long=11.0),
            make_planet(Planet.SUN, 15.0, speed_long=1.0)
        ]
        
        assert rule.evaluate(planets, []) is True


class TestRuleMatch:
    """Test rule match model."""
    
    def test_match_percentage(self):
        """Calculate match percentage correctly."""
        match = RuleMatch(
            rule_name="Test",
            timestamp=datetime.now(timezone.utc),
            matched_conditions=3,
            total_conditions=4
        )
        
        assert match.match_percentage == 75.0


class TestTimeRangeScanning:
    """Test scanning time ranges for events."""
    
    def test_scan_finds_matches(self):
        """Scan detects rule matches over time range."""
        rule = EventRule(
            name="Moon Fast",
            conditions=[
                SpeedCondition(planet=Planet.MOON, operator=">", value=12.0)
            ]
        )
        
        # Mock callback that returns fast Moon every time
        def get_data(dt):
            planets = [make_planet(Planet.MOON, 100.0, speed_long=13.0)]
            return planets, []
        
        start = datetime(2024, 1, 1, tzinfo=timezone.utc)
        end = datetime(2024, 1, 3, tzinfo=timezone.utc)
        
        matches = scan_time_range(start, end, [rule], interval_hours=24.0, get_chart_data_callback=get_data)
        
        # Should find 3 matches (Jan 1, 2, 3)
        assert len(matches) == 3
        assert all(m.rule_name == "Moon Fast" for m in matches)
    
    def test_scan_no_matches(self):
        """Scan returns empty when no matches."""
        rule = EventRule(
            name="Moon Slow",
            conditions=[
                SpeedCondition(planet=Planet.MOON, operator="<", value=5.0)
            ]
        )
        
        # Moon always fast
        def get_data(dt):
            planets = [make_planet(Planet.MOON, 100.0, speed_long=13.0)]
            return planets, []
        
        start = datetime(2024, 1, 1, tzinfo=timezone.utc)
        end = datetime(2024, 1, 2, tzinfo=timezone.utc)
        
        matches = scan_time_range(start, end, [rule], interval_hours=24.0, get_chart_data_callback=get_data)
        
        assert len(matches) == 0
