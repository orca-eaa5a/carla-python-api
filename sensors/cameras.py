from sensor import *

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
        self.sensor.listen(lambda data:DepthCameraSensor.callback)
    
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

