from sensor import *

class Advanced(Sensor):
    @abstractmethod
    def register_eventlistener(self, cb):
        pass

    def __init__(self, parent_actor) -> None:
        super().__init__(parent_actor)

class CollisionSensor(Advanced):
    def __init__(self, parent_actor) -> None:
        super().__init__(parent_actor)
        self.history = []
        self.blueprint = self.get_blueprint()
        self.sensor = self.world.spawn_actor(self.blueprint, carla.Transform(), attach_to=self._parent_actor)
        pass

    def get_blueprint(self, sensor_type='sensor.other.collision'):
        return super().get_bluepoint(sensor_type)
    
    def register_eventlistener(self, cb):
        # carla.CollisionEvent
        self.sensor.listen(lambda evt: cb(evt))

class LaneInvasionSensor(Advanced):
    def __init__(self, parent_actor) -> None:
        super().__init__(parent_actor)
        if parent_actor.type_id.startswith("vehicle."):
            raise ValueError("target object is not a vehicle, we can only attach the Lane Invasion Sensor to vehicle object")
        self.blueprint = self.get_blueprint()
        self.sensor = self.world.spawn_actor(self.blueprint, carla.Transform(), attach_to=self._parent_actor)
        
    def get_blueprint(self, sensor_type='sensor.other.lane_invasion'):
        return super().get_bluepoint(sensor_type)
    
    def register_eventlistener(self, cb):
        # @evt: carla.LaneInvasionEvent
        self.sensor.listen(lambda evt: cb(evt))

class ObstacleDetectionSensor(Advanced):
    def __init__(self, parent_actor) -> None:
        super().__init__(parent_actor)
        self.remain_distance = 0.0
        self.blueprint = self.get_blueprint()
        self.sensor = self.world.spawn_actor(self.blueprint, carla.Transform(), attach_to=self._parent_actor)
    
    def get_blueprint(self, sensor_type='sensor.other.obstacle'):
        return super().get_blueprint(sensor_type)
    
    def register_eventlistener(self, cb):
        # @evt: carla.ObstacleDetectionEvent
        self.sensor.listen(lambda evt: cb(evt))
    
    @set_sensor_attribute_decorator
    def set_distance(self, distance=5.0):
        # Distance to trace.
        self.sensor.__setattr__('distance', distance)
    
    @set_sensor_attribute_decorator
    def set_hit_radius(self, hit_radius=0.5):
        # Radius of the trace.
        self.sensor.__setattr__('hit_radius', hit_radius)

    @set_sensor_attribute_decorator
    def set_only_dynamics(self, only_dynamics=False):
        # If true, the trace will only consider dynamic objects.
        self.sensor.__setattr__('only_dynamics', only_dynamics)


# TODO implement RssSensor

class RssSensor(Advanced):
    # this only support in Linux environment
    # The RSS sensor uses world information, and a RSS library to 'make safety checks (safety calcuration)' on a vehicle
    def __init__(self, parent_actor) -> None:
        super().__init__(parent_actor)
        self.blueprint = self.get_blueprint()
        self.sensor = self.world.spawn_actor(self.blueprint, carla.Transform(), attach_to=self._parent_actor)
    
    def get_blueprint(self, sensor_type='sensor.other.rss'):
        return super().get_blueprint(sensor_type)
    
    def register_eventlistener(self, cb):
        # @evt: carla.RssResponse
        self.sensor.listen(lambda evt: cb(evt))