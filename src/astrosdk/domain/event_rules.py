"""
Custom Event Rule Engine

Enables JSON-driven detection of custom astronomical patterns.
Users can define rules with conditions (aspects, dignities, speed, etc.)
and scan time ranges for matching events.

Example:
    rule = EventRule(
        name="Venus Exalted + Moon Trine",
        conditions=[
            DignityCondition(planet=Planet.VENUS, dignity=DignityType.EXALTATION),
            AspectCondition(planet1=Planet.MOON, planet2=Planet.VENUS, aspect="trine")
        ],
        logic=LogicOperator.AND
    )
    
    matches = scan_time_range(start, end, [rule])
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Union, Literal, Optional
from enum import Enum
from datetime import datetime, timedelta

from ..core.constants import Planet
from .planet import PlanetPosition
from .aspect import Aspect
from .dignity import DignityType, calculate_dignity
from .combustion import CombustionState, calculate_combustion


class LogicOperator(str, Enum):
    """Logical operator for combining conditions."""
    AND = "AND"
    OR = "OR"


class ConditionType(str, Enum):
    """Types of conditions that can be evaluated."""
    ASPECT = "aspect"
    DIGNITY = "dignity"
    COMBUSTION = "combustion"
    SPEED = "speed"
    LONGITUDE = "longitude"
    RETROGRADE = "retrograde"


class AspectCondition(BaseModel):
    """Condition checking for a specific aspect between two planets."""
    model_config = ConfigDict(frozen=True)
    
    type: Literal[ConditionType.ASPECT] = ConditionType.ASPECT
    planet1: Planet
    planet2: Planet
    aspect: str = Field(description="Aspect name: conjunction, opposition, trine, square, sextile")
    orb: Optional[float] = Field(default=None, description="Custom orb in degrees")
    
    def evaluate(self, aspects: List[Aspect]) -> bool:
        """Check if this aspect exists in the provided aspects list."""
        for asp in aspects:
            # Check both orderings (A-B and B-A)
            if ((asp.p1 == self.planet1 and asp.p2 == self.planet2) or
                (asp.p1 == self.planet2 and asp.p2 == self.planet1)):
                if asp.type.lower() == self.aspect.lower():
                    if self.orb is None or abs(asp.orb) <= self.orb:
                        return True
        return False


class DignityCondition(BaseModel):
    """Condition checking for a planet's essential dignity."""
    model_config = ConfigDict(frozen=True)
    
    type: Literal[ConditionType.DIGNITY] = ConditionType.DIGNITY
    planet: Planet
    dignity: DignityType
    
    def evaluate(self, planets: List[PlanetPosition]) -> bool:
        """Check if planet has the specified dignity."""
        for p in planets:
            if p.planet == self.planet:
                # Use PlanetPosition's sign_degree computed field
                result = calculate_dignity(p.planet, p.sign, p.sign_degree)
                return result.type == self.dignity
        return False


class CombustionCondition(BaseModel):
    """Condition checking for a planet's combustion state."""
    model_config = ConfigDict(frozen=True)
    
    type: Literal[ConditionType.COMBUSTION] = ConditionType.COMBUSTION
    planet: Planet
    state: CombustionState
    
    def evaluate(self, planets: List[PlanetPosition]) -> bool:
        """Check if planet has the specified combustion state."""
        sun_long = None
        planet_long = None
        
        for p in planets:
            if p.planet == Planet.SUN:
                sun_long = p.longitude
            if p.planet == self.planet:
                planet_long = p.longitude
        
        if sun_long is None or planet_long is None:
            return False
        
        result = calculate_combustion(planet_long, sun_long, self.planet)
        return result.state == self.state


class SpeedCondition(BaseModel):
    """Condition checking planetary speed."""
    model_config = ConfigDict(frozen=True)
    
    type: Literal[ConditionType.SPEED] = ConditionType.SPEED
    planet: Planet
    operator: Literal["<", ">", "==", "<=", ">="]
    value: float = Field(description="Speed in degrees per day")
    
    def evaluate(self, planets: List[PlanetPosition]) -> bool:
        """Check if planet's speed matches the condition."""
        for p in planets:
            if p.planet == self.planet:
                if self.operator == "<":
                    return p.speed_long < self.value
                elif self.operator == ">":
                    return p.speed_long > self.value
                elif self.operator == "==":
                    return abs(p.speed_long - self.value) < 0.01
                elif self.operator == "<=":
                    return p.speed_long <= self.value
                elif self.operator == ">=":
                    return p.speed_long >= self.value
        return False


class RetrogradeCondition(BaseModel):
    """Condition checking if a planet is retrograde."""
    model_config = ConfigDict(frozen=True)
    
    type: Literal[ConditionType.RETROGRADE] = ConditionType.RETROGRADE
    planet: Planet
    is_retrograde: bool = True
    
    def evaluate(self, planets: List[PlanetPosition]) -> bool:
        """Check if planet is retrograde (speed_long < 0)."""
        for p in planets:
            if p.planet == self.planet:
                actual_retrograde = p.speed_long < 0
                return actual_retrograde == self.is_retrograde
        return False


class LongitudeCondition(BaseModel):
    """Condition checking if planet is within a longitude range."""
    model_config = ConfigDict(frozen=True)
    
    type: Literal[ConditionType.LONGITUDE] = ConditionType.LONGITUDE
    planet: Planet
    min_longitude: float = Field(ge=0.0, lt=360.0)
    max_longitude: float = Field(ge=0.0, lt=360.0)
    
    def evaluate(self, planets: List[PlanetPosition]) -> bool:
        """Check if planet longitude is in range."""
        for p in planets:
            if p.planet == self.planet:
                # Handle wraparound cases (e.g., 350-10 degrees)
                if self.min_longitude <= self.max_longitude:
                    return self.min_longitude <= p.longitude <= self.max_longitude
                else:
                    # Range wraps around 0
                    return p.longitude >= self.min_longitude or p.longitude <= self.max_longitude
        return False


# Union type for all condition types
RuleCondition = Union[
    AspectCondition,
    DignityCondition,
    CombustionCondition,
    SpeedCondition,
    RetrogradeCondition,
    LongitudeCondition
]


class EventRule(BaseModel):
    """
    A complete event detection rule with multiple conditions.
    
    Conditions are combined using the specified logic operator (AND/OR).
    """
    model_config = ConfigDict(frozen=True)
    
    name: str = Field(description="Human-readable rule name")
    conditions: List[RuleCondition] = Field(min_length=1)
    logic: LogicOperator = LogicOperator.AND
    description: Optional[str] = None
    
    def evaluate(self, planets: List[PlanetPosition], aspects: List[Aspect]) -> bool:
        """
        Evaluate all conditions against the current chart state.
        
        Args:
            planets: List of planet positions
            aspects: List of aspects
        
        Returns:
            True if the rule matches, False otherwise
        """
        results = []
        
        for condition in self.conditions:
            if isinstance(condition, AspectCondition):
                results.append(condition.evaluate(aspects))
            else:
                # All other conditions use planets
                results.append(condition.evaluate(planets))
        
        if self.logic == LogicOperator.AND:
            return all(results)
        else:  # OR
            return any(results)


class RuleMatch(BaseModel):
    """A detected event that matched a rule."""
    model_config = ConfigDict(frozen=True)
    
    rule_name: str
    timestamp: datetime
    matched_conditions: int
    total_conditions: int
    
    @property
    def match_percentage(self) -> float:
        """Percentage of conditions that matched (useful for partial matches)."""
        return (self.matched_conditions / self.total_conditions) * 100.0


def evaluate_rule_at_time(
    rule: EventRule,
    planets: List[PlanetPosition],
    aspects: List[Aspect]
) -> bool:
    """
    Evaluate a single rule at a specific time.
    
    Args:
        rule: The event rule to evaluate
        planets: Planet positions at this time
        aspects: Aspects at this time
    
    Returns:
        True if rule matches, False otherwise
    """
    return rule.evaluate(planets, aspects)


def scan_time_range(
    start_time: datetime,
    end_time: datetime,
    rules: List[EventRule],
    interval_hours: float = 24.0,
    get_chart_data_callback = None
) -> List[RuleMatch]:
    """
    Scan a time range for rule matches.
    
    Args:
        start_time: Start of scan range
        end_time: End of scan range
        rules: List of rules to check
        interval_hours: Time step in hours (default: 24 = daily)
        get_chart_data_callback: Function(datetime) -> (planets, aspects)
                                  Must be provided to get chart data at each time
    
    Returns:
        List of RuleMatch objects for all detected events
    
    Example:
        >>> from astrosdk import calculate_natal_chart, calculate_aspects
        >>> 
        >>> def get_data(dt):
        >>>     chart = calculate_natal_chart(dt, lat, lon)
        >>>     aspects = calculate_aspects(chart.planets)
        >>>     return chart.planets, aspects
        >>> 
        >>> matches = scan_time_range(start, end, [rule], get_chart_data_callback=get_data)
    """
    if get_chart_data_callback is None:
        raise ValueError("get_chart_data_callback must be provided")
    
    matches = []
    current = start_time
    delta = timedelta(hours=interval_hours)
    
    while current <= end_time:
        planets, aspects = get_chart_data_callback(current)
        
        for rule in rules:
            if rule.evaluate(planets, aspects):
                match = RuleMatch(
                    rule_name=rule.name,
                    timestamp=current,
                    matched_conditions=len(rule.conditions),
                    total_conditions=len(rule.conditions)
                )
                matches.append(match)
        
        current += delta
    
    return matches
