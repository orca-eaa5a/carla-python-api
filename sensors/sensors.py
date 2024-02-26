from sensor import *
#############################################################################################
#   GnssSensor                                                                              #
#############################################################################################

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
        self.sensor.listen(lambda data: GnssSensor.callback(weakref.ref(self), data))

#############################################################################################
#   IMUSensor                                                                               #
#############################################################################################

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

#############################################################################################
#   Lidar & Radar Sensor                                                                    #
#############################################################################################

class LidarSensor(Sensor):
    
    @staticmethod
    def get_points(sensor_data) -> List[carla.LidarDetection]:
        # Each of these represents one of the points in the cloud with its location and its associated intensity.
        """
        carla.LidarDetection
        @ point : Point in xyz coordinates
        @ intensity : Computed intensity for this point as a scalar value between [0.0 , 1.0].
                        반사되어 돌아온 신호의 강도 (반사도 세기)
                        intensity가 크다 => 물체가 가까이 있다 (물체의 표면에 따라 다를 수 있음)
        """
        return list(sensor_data)
    
    @staticmethod
    def callback(weakself, sensor_data:carla.LidarMeasurement):
        self = weakself()
        if not self:
            return
        self.channels = sensor_data.channels
        self.horizontal_angle = sensor_data.horizontal_angle
        self.raw_data = sensor_data.raw_data
        if self.save_lidar_map:
            path = os.path.join(os.pardir(__file__), 'lidar')
            if not os.path.exists(path):
                os.makedirs(path)
            sensor_data.save_to_disk(path)

    def __init__(self, parent_actor) -> None:
        super().__init__(parent_actor)
        self.channels = 0
        self.horizontal_angle = 0.0
        self.raw_data = b''
        self.save_lidar_map = False

    def get_blueprint(self, sensor_type='sensor.lidar.ray_cast'):
        return super().get_bluepoint(sensor_type)

    def register_sensing_callback(self):
        self.sensor.listen(lambda data: IMUSensor.callback(weakref.ref(self), data))

    def on_save(self):
        self.save_lidar_map = True
    
    def save_off(self):
        self.save_lidar_map = False
    
    """
    carla.LidarMeasurement attributes
    """

    @set_sensor_attribute_decorator
    def set_channels(self, channels=32):
        # Number of lasers shot
        self.sensor.__setattr__('channel', channels)

    @set_sensor_attribute_decorator
    def set_range(self, _range=10.0):
        # Maximum distance to measure/raycast in 'meters' (centimeters for CARLA 0.9.6 or previous).
        self.sensor.__setattr__('range', _range)

    @set_sensor_attribute_decorator
    def set_points_per_second(self, points_per_seconds=56000):
        # Points generated by all lasers per second.
        self.sensor.__setattr__('points_per_seconds', points_per_seconds)
    
    @set_sensor_attribute_decorator
    def set_rotation_frequency(self, rotation_frequency=10.0):
        # LIDAR rotation frequency.
        self.sensor.__setattr__('rotation_frequency', rotation_frequency)

    @set_sensor_attribute_decorator
    def set_upper_fov(self, upper_fov=10.0):
        # Angle in degrees of the highest laser.
        self.sensor.__setattr__('upper_fov', upper_fov)
    
    @set_sensor_attribute_decorator
    def set_lower_fov(self, lower_fov=-30.0):
        # Angle in degrees of the lowest laser.
        self.sensor.__setattr__('lower_fov', lower_fov)

    @set_sensor_attribute_decorator
    def set_horizontal_fov(self, horizontal_fov=360.0):
        # Angle in degrees of the lowest laser.
        self.sensor.__setattr__('horizontal_fov', horizontal_fov)

    @set_sensor_attribute_decorator
    def set_atmosphere_attenuation_rate(self, atmosphere_attenuation_rate=0.004):
        # Coefficient that measures the LIDAR instensity loss per meter.
        self.sensor.__setattr__('atmosphere_attenuation_rate', atmosphere_attenuation_rate)

    @set_sensor_attribute_decorator
    def set_dropoff_general_rate(self, dropoff_general_rate=0.45):
        # General proportion of points that are randomy dropped.
        self.sensor.__setattr__('dropoff_general_rate', dropoff_general_rate)
    
    @set_sensor_attribute_decorator
    def set_dropoff_intensity_limit(self, dropoff_intensity_limit=0.8):
        # For the intensity based drop-off, the threshold intensity value above which no points are dropped.
        self.sensor.__setattr__('dropoff_intensity_limit', dropoff_intensity_limit)
    
    @set_sensor_attribute_decorator
    def set_dropoff_zero_intensity(self, dropoff_zero_intensity=0.4):
        # For the intensity based drop-off, the probability of each point with zero intensity being dropped.
        self.sensor.__setattr__('dropoff_zero_intensity', dropoff_zero_intensity)

    @set_sensor_attribute_decorator
    def set_noise_stddev(self, noise_stddev=0.0):
        # Standard deviation of the noise model to disturb each point along the vector of its raycast.
        self.sensor.__setattr__('noise_stddev', noise_stddev)
        

class RadarSensor(Sensor):
    # creates a conic view that is translated to a 2D point map of the elements in sight
    # 시뮬레이션에서, 4D Point Cloud 생성을 목적으로 한다면, Radar보다 Lidar 센서를 사용
    @staticmethod
    def get_points(sensor_data) -> List[carla.RadarDetection]:
        # carla.RadarDetection, which specifies their polar coordinates, distance and velocity.
        """
        carla.RadarDetection
        @ altitude : Altitude angle in radians.
        @ azimuth : Azimuth angle in radians.
        @ depth : Distance in meters.
        @ velocity : Velocity towards the sensor.
        """
        return list(sensor_data)
    
    @staticmethod
    def callback(weakself, sensor_data:carla.RadarMeasurement):
        pass

    def __init__(self, parent_actor) -> None:
        super().__init__(parent_actor)
    
    def get_blueprint(self, sensor_type='sensor.other.radar'):
        return super().get_blueprint(sensor_type)
    
    def register_sensing_callback(self):
        self.sensor.listen(lambda data: RadarSensor.callback(weakref.ref(self), data))
    
    @set_sensor_attribute_decorator
    def set_horizontal_fov(self, horizontal_fov=30.0):
        # Horizontal field of view in degrees.
        self.sensor.__setattr__('horizontal_fov', horizontal_fov)
    
    @set_sensor_attribute_decorator
    def set_points_per_second(self, points_per_second=1500):
        # Points generated by all lasers per second.
        self.sensor.__setattr__('points_per_second', points_per_second)

    @set_sensor_attribute_decorator
    def set_range(self, _range=100):
        # Maximum distance to measure/raycast in meters.
        self.sensor.__setattr__('range', _range)
    
    @set_sensor_attribute_decorator
    def set_vertical_fov(self, vertical_fov=30.0):
        # Vertical field of view in degrees.
        self.sensor.__setattr__('vertical_fov', vertical_fov)