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
        self.raw_color = self.colorSensor.getRawColor()
        print(self.raw_color.red, self.raw_color.green, self.raw_color.blue)
        if self.raw_color.blue > 130:
            return True
        else:
            return False
            
