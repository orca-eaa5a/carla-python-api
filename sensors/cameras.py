from sensor import *

#############################################################################################
#   RGBCameraSensor                                                                         #
#    - acts as a regular camera capturing images                                            #
#############################################################################################

class RGBCameraSensor(Sensor):
    @staticmethod
    def callback(weakself, sensor_data:carla.Image):
        # https://carla.readthedocs.io/en/latest/python_api/#carla.Image
        self = weakself()
        if not self:
            return
        self.raw_data = sensor_data.raw_data
        if self.save_image:
            path = os.path.join(os.pardir(__file__), 'lidar')
            if not os.path.exists(path):
                os.makedirs(path)
            sensor_data.save_to_disk(path)
        
    def __init__(self, parent_actor) -> None:
        super().__init__(parent_actor)
        self.raw_data = b''
        self.save_image = False

    def get_blueprint(self, sensor_type='sensor.camera.rgb'):
        return super().get_blueprint(sensor_type)
    def register_sensing_callback(self):
        self.sensor.listen(lambda data:RGBCameraSensor.callback(weakref.ref(self), data))

    def on_save(self):
        self.save_image = True
    
    def save_off(self):
        self.save_image = False
    
    @set_sensor_attribute_decorator
    def set_image_width(self, image_size_x):
        self.sensor.__setattr__('image_size_x', image_size_x)

    @set_sensor_attribute_decorator
    def set_image_height(self, image_size_y):
        self.sensor.__setattr__('image_size_y', image_size_y)
    
    @set_sensor_attribute_decorator
    def set_gamma(self, gamma=2.2):
        # gamma가 작아지면 이미지가 밝아지고, gamma가 커지면 이미지가 어두워짐
        # 2.2는 사람 눈에 최적화된 standard gamma value
        self.sensor.__setattr__('gamma', gamma)
    
    @set_sensor_attribute_decorator
    def set_shutter_speed(self, shutter_speed):
        # The camera shutter speed in seconds (1.0/s).
        self.sensor.__setattr__('shutter_speed', shutter_speed)
    
    pass

#############################################################################################
#   DepthCameraSensor                                                                       #
#############################################################################################

class DepthCameraSensor(Sensor):
    @staticmethod
    def callback(weakself, sensor_data):
        self = weakself()
        if not self:
            return
        
    def __init__(self, parent_actor) -> None:
        super().__init__(parent_actor)
    
    def get_blueprint(self, sensor_type='sensor.camera.depth'):
        return super().get_blueprint(sensor_type)
    
    def register_sensing_callback(self):
        self.sensor.listen(lambda data:DepthCameraSensor.callback(weakref.ref(self), data))
    
    @set_sensor_attribute_decorator
    def set_image_width(self, image_size_x=800):
        # Image width in pixels.
        self.sensor.__setattr__('image_size_x', image_size_x)
    
    @set_sensor_attribute_decorator
    def set_image_height(self, image_size_y=600):
        # Image height in pixels
        self.sensor.__setattr__('image_size_y', image_size_y)

    @set_sensor_attribute_decorator
    def set_fov(self, fov=90.0):
        # field of view
        # https://www.youtube.com/watch?v=jf4KajOSkPk
        self.sensor.__setattr__('fov', fov)

