import os
import math
from typing import List
import weakref
from abc import abstractmethod

import carla

def set_sensor_attribute_decorator(func):
    def wrapper(self, *args, **kwargs):
        if not self.sensor:
            raise ValueError("sensor is empty")
        return func(self, *args, **kwargs)
    return wrapper

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