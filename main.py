import sys
import carla
import random

def get_actor_display_name(actor, truncate=250):
    name = ' '.join(actor.type_id.replace('_', '.').title().split('.')[1:])
    return (name[:truncate - 1] + u'\u2026') if len(name) > truncate else name

def get_vehicleactor_blueprint(world):
    vehicle_blueprints = list(world.get_blueprint_library().filter("vehicle.*"))
    if not vehicle_blueprints:
        raise ValueError("No availiable vehicle blueprint")
    return vehicle_blueprints


class SimVehicle(object):
    def __init__(self, world:carla.World) -> None:
        self.world = world
        self.blueprint = None
        self.actor = None
        pass

    @property
    def role_name(self):
        return self.blueprint.__getattribute__('role_name')
    
    @property
    def terramechanics(self):
        return self.blueprint.__getattribute__('terramechanics')
    
    @property
    def color(self):
        return self.blueprint.__getattribute__('color')
    
    @property
    def driver_id(self):
        return self.blueprint.__getattribute__('driver_id')
    
    @property
    def invincible(self):
        return self.blueprint.__getattribute__('is_invincible')
    
    @property
    def max_speed(self):
        return float(self.blueprint.get_attribute('speed').recommended_values[1])

    @property
    def max_speed_fast(self):
        return float(self.blueprint.get_attribute('speed').recommended_values[2])

    def get_blueprint_list(self):
        vehicle_blueprints = list(self.world.get_blueprint_library().filter("vehicle.*"))
        if not vehicle_blueprints:
            raise ValueError("No availiable vehicle blueprint")
        return vehicle_blueprints

    def get_random_blueprint(self):
        blueprints = self.get_blueprint_list()
        return random.choice(blueprints)

    def setup_attribute(self):
        self.blueprint.set_attribute('role_name', "vehicle")
        if self.blueprint.has_attribute('terramechanics'):
            self.blueprint.set_attribute('terramechanics', 'true') # recommended
        if self.blueprint.has_attribute('terramechanics'):
            self.blueprint.set_attribute('terramechanics', 'true') # recommended
        if self.blueprint.has_attribute('color'):
            color = random.choice(self.blueprint.get_attribute('color').recommended_values)
            self.blueprint.set_attribute('color', color)
        if self.blueprint.has_attribute('driver_id'):
            driver_id = random.choice(self.blueprint.get_attribute('driver_id').recommended_values)
            self.blueprint.set_attribute('driver_id', driver_id)
        if self.blueprint.has_attribute('is_invincible'):
            self.blueprint.set_attribute('is_invincible', 'true') # recommended

    def setup_actor(self, map:carla.Map):
        if self.actor is not None:
            # Returns the actor's transform (location and rotation)
            spawn_point:carla.Transform = self.actor.get_transform()
            spawn_point.location.z += 2.0 # <-- ??
            spawn_point.rotation.roll = 0.0
            spawn_point.rotation.pitch = 0.0
            self.destroy()
            self.actor:carla.Actor = self.world.try_spawn_actor(self.blueprint, spawn_point)
            # self.show_vehicle_telemetry = False # <-- ??
            # self.modify_vehicle_physics(self.actor) < -- ??

        threshold = 0

        while self.actor is None and threshold < 5:
            if not map.get_spawn_points():
                print('There are no spawn points available in your map/town.')
                print('Please add some Vehicle Spawn Point to your UE4 scene.')
                sys.exit(1)
            spawn_points = map.get_spawn_points() # get recommended spawn points list
            spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
            self.actor = self.world.try_spawn_actor(self.blueprint, spawn_point)
            # self.show_vehicle_telemetry = False # <-- ??
            # self.modify_vehicle_physics(self.actor) < -- ??
            threshold += 1
        
        if not self.actor:
            raise ValueError("fail to setup vehicle actor")

        return True


class SimWorld(object):
    def __init__(self, client, hud, args) -> None:
        self.world:carla.World = client.get_world()
        self.vehicle:SimVehicle = SimVehicle(self.world)
        # The client needs to make a request to the server to get the .xodr map file
        # The map object contains recommended spawn points for the creation of vehicles.

        self.map:carla.Map = self.world.get_map()
        self.map_layer_names = [
            carla.MapLayer.NONE,
            carla.MapLayer.Buildings,
            carla.MapLayer.Decals,
            carla.MapLayer.Foliage,
            carla.MapLayer.Ground,
            carla.MapLayer.ParkedVehicles,
            carla.MapLayer.Particles,
            carla.MapLayer.Props,
            carla.MapLayer.StreetLights,
            carla.MapLayer.Walls,
            carla.MapLayer.All
        ]
        self.current_map_layer = 0
        pass

    def setup(self):
        cam_index = self.camera_manager.index if self.camera_manager is not None else 0
        cam_pos_index = self.camera_manager.transform_index if self.camera_manager is not None else 0
        self.vehicle.blueprint = self.vehicle.get_random_blueprint()
        self.vehicle.setup_attribute()
        self.vehicle.setup_actor(self.map)


        

    

def main():
    try:
        host = "127.0.0.1"
        port = 2000

        client = carla.Client(host, port)
        client.set_timeout(3.0) # An error will be returned if connection fails. (3 sec)
        
        


    except Exception as e:
        pass
