from pydantic import BaseModel, Field, ConfigDict

class AccelerationData(BaseModel):
    """
    Acceleration state for a planetary body.
    """
    model_config = ConfigDict(frozen=True)
    
    longitude_accel: float
    latitude_accel: float
    distance_accel: float
    
    @property
    def is_accelerating(self) -> bool:
        return self.longitude_accel > 0
    
    @property
    def is_decelerating(self) -> bool:
        return self.longitude_accel < 0
    
    @property
    def is_near_station(self) -> bool:
        return abs(self.longitude_accel) < 0.01

def calculate_acceleration(
    speed_long_before: float, speed_long_after: float,
    speed_lat_before: float, speed_lat_after: float,
    speed_dist_before: float, speed_dist_after: float,
    time_delta: float
) -> AccelerationData:
    """
    Pure calculation of acceleration from two speed snapshots.
    """
    lon_accel = (speed_long_after - speed_long_before) / (2 * time_delta)
    lat_accel = (speed_lat_after - speed_lat_before) / (2 * time_delta)
    dist_accel = (speed_dist_after - speed_dist_before) / (2 * time_delta)
    
    return AccelerationData(
        longitude_accel=lon_accel,
        latitude_accel=lat_accel,
        distance_accel=dist_accel
    )
