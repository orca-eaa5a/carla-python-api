import math
import weakref
from abc import abstractmethod

import carla

class Sensor(object):
    @property
    def world(self):
        world = self._parent_actor.get_world()
        if not world:
            raise ValueError("world is None")
        return world
    
    @abstractmethod
    def get_blueprint(self, sensor_type):
        try:
            bp = self.world.get_blueprint_library().find(sensor_type)
        except Exception as e:
            raise(str(e))
        self.sensor = self.world.spawn_actor(bp, carla.Transform(), attach_to=self._parent_actor)
        if not self.sensor:
            return False
        return True
    
    def __init__(self, parent_actor) -> None:
        self.sensor = None
        self._parent_actor = parent_actor
        self.blueprint = None
        pass

class Detector(Sensor):
    @abstractmethod
    def register_eventlistener(self, cb):
        pass

class CollisionSensor(Detector):
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

class LaneInvasionSensor(Detector):
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

class ObstacleDetectionSensor(Detector):
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

class GnssSensor(Sensor):
    @staticmethod
    def callback(weakself, sensor_data):
        self = weakself()
        if not self:
            return
        self.alt = sensor_data.altitude
        self.lat = sensor_data.latitude
        self.lon = sensor_data.longitude

    def __init__(self, parent_actor) -> None:
        super().__init__(parent_actor)
        self.alt = 0.0
        self.lat = 0.0
        self.lon = 0.0
        self.blueprint = self.get_blueprint()

    def get_blueprint(self, sensor_type='sensor.other.gnss'):
        return super().get_bluepoint(sensor_type)

    def register_sensing_callback(self):
        self.sensor.listen(lambda data: IMUSensor.callback(weakref.ref(self), data))

class IMUSensor(Sensor):
    @staticmethod
    def callback(weakself, sensor_data):
        self = weakself()
        if not self:
            return
        limits = (-99.9, 99.9)
        self.accelerometer = (
            max(limits[0], min(limits[1], sensor_data.accelerometer.x)),
            max(limits[0], min(limits[1], sensor_data.accelerometer.y)),
            max(limits[0], min(limits[1], sensor_data.accelerometer.z)))
        self.gyroscope = (
            max(limits[0], min(limits[1], math.degrees(sensor_data.gyroscope.x))),
            max(limits[0], min(limits[1], math.degrees(sensor_data.gyroscope.y))),
            max(limits[0], min(limits[1], math.degrees(sensor_data.gyroscope.z))))
        self.compass = math.degrees(sensor_data.compass)

    def __init__(self, parent_actor) -> None:
        super().__init__(parent_actor)
        self.accelerometer = (0.0, 0.0, 0.0)
        self.gyroscope = (0.0, 0.0, 0.0)
        self.compass = 0.0
        self.blueprint = self.get_blueprint()
        self.register_sensing_callback()

    def get_blueprint(self, sensor_type='sensor.other.imu'):
        return super().get_bluepoint(sensor_type)

    def register_sensing_callback(self):
        self.sensor.listen(lambda data: IMUSensor.callback(weakref.ref(self), data))

class LidarSensor(Sensor):
    def __init__(self, parent_actor) -> None:
        super().__init__(parent_actor)

class RadarSensor(Sensor):
    def __init__(self, parent_actor) -> None:
        super().__init__(parent_actor)
    



# class RadarSensor(Sensor):
#     def __init__(self, parent_actor) -> None:
#         super().__init__(parent_actor)
#         bound_x = 0.5 + self.parent_actor.bounding_box.extent.x
#         bound_y = 0.5 + self.parent_actor.bounding_box.extent.y
#         bound_z = 0.5 + self.parent_actor.bounding_box.extent.z