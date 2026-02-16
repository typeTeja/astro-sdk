import pytest
from datetime import datetime, timezone
from astrosdk.core.time import Time
from astrosdk.core.ephemeris import Ephemeris
from astrosdk.core.constants import Planet, SiderealMode
from astrosdk.services.node_service import NodeService

@pytest.fixture
def ephemeris():
    return Ephemeris()

@pytest.fixture
def node_service(ephemeris):
    return NodeService(ephemeris)

class TestNodeService:
    def test_lunar_nodes(self, node_service):
        """Test calculation of North and South lunar nodes."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        
        # True Node
        north, south = node_service.calculate_lunar_nodes(time, true_node=True)
        assert north.planet == Planet.TRUE_NODE
        assert abs((north.longitude + 180) % 360 - south.longitude) < 0.001
        
        # Mean Node
        north_m, south_m = node_service.calculate_lunar_nodes(time, true_node=False)
        assert north_m.planet == Planet.MEAN_NODE
        assert abs((north_m.longitude + 180) % 360 - south_m.longitude) < 0.001
        
    def test_lilith(self, node_service):
        """Test calculation of Lilith (Lunar Apogee)."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        
        # Mean Lilith
        lilith = node_service.calculate_lilith(time, true_lilith=False)
        assert lilith.planet == Planet.LILITH_MEAN
        assert 0 <= lilith.longitude < 360
        
        # True Lilith
        lilith_t = node_service.calculate_lilith(time, true_lilith=True)
        assert lilith_t.planet == Planet.LILITH_TRUE
        assert lilith.longitude != lilith_t.longitude

    def test_planetary_nodes(self, node_service):
        """Test planetary node calculation (Mars)."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        
        nodes = node_service.calculate_planetary_nodes(time, Planet.MARS)
        assert "ascending_node" in nodes
        assert "descending_node" in nodes
        assert 0 <= nodes["ascending_node"] < 360
        assert 0 <= nodes["descending_node"] < 360

    def test_planetary_apsides(self, node_service):
        """Test perihelion/aphelion calculation (Jupiter)."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        
        apsides = node_service.calculate_apsides(time, Planet.JUPITER)
        assert "perihelion" in apsides
        assert "aphelion" in apsides
        assert 0 <= apsides["perihelion"] < 360
        assert 0 <= apsides["aphelion"] < 360
        
    def test_node_service_sidereal(self, ephemeris, node_service):
        """Test that NodeService respects sidereal mode settings."""
        time = Time(datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc))
        
        ephemeris.set_sidereal_mode(SiderealMode.LAHIRI)
        north_l, _ = node_service.calculate_lunar_nodes(time)
        
        ephemeris.set_sidereal_mode(SiderealMode.FAGAN_BRADLEY)
        north_f, _ = node_service.calculate_lunar_nodes(time)
        
        assert north_l.longitude != north_f.longitude
