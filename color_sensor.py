from rev import ColorSensorV3
from wpilib import I2C 

class ColorSensor():
    def __init__(self):
        """
        Initializer for the Vision module.

        :param camera: Name of the camera. Can be found in the PhotonVision dashboard.
        :type camera: str
        :param colorSensor: Location of the color sensor port on the board.
        :type colorSensor: Port
        """
        self.colorSensor = ColorSensorV3(I2C.Port.kMXP)
    
    def has_ring(self):
        """
        Check for a ring in the robot.
        """
        raw_color = self.colorSensor.getRawColor()
        self.check_if_disconnected(raw_color)
        print(raw_color.red, raw_color.green, raw_color.blue)
        if raw_color.blue > 130:
            return True
        else:
            return False
        
    def check_if_disconnected(self, raw_color):
        if raw_color.red == 0 and raw_color.green == 0 and raw_color.blue == 0:
            self.color_sensor = ColorSensorV3(I2C.Port.kMXP)

            
