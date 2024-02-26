from rev import ColorSensorV3
from wpilib import I2C 
from wpilib.shuffleboard import Shuffleboard

class ColorSensor():
    def __init__(self):
        """
        Initializer for the Vision module.

        :param camera: Name of the camera. Can be found in the PhotonVision dashboard.
        :type camera: str
        :param colorSensor: Location of the color sensor port on the board.
        :type colorSensor: Port
        """
        self.color_sensor = ColorSensorV3(I2C.Port.kMXP)
        self.rgb_entry = Shuffleboard.getTab("ColorSensor").add(f"Color Sensor RGB", "0, 0, 0").getEntry()
    
    def detects_ring(self):
        """
        Check for a ring in the robot.
        """
        raw_color = self.color_sensor.getRawColor()
        self.rgb_entry.setString(f"{raw_color.red}, {raw_color.green}, {raw_color.blue}") 
        raw_color = self._check_if_disconnected(raw_color) 
        if raw_color.blue > 125:
            return True
        else:
            return False
        
    def _check_if_disconnected(self, raw_color):
        if raw_color.red == 0 and raw_color.green == 0 and raw_color.blue == 0:
            self.color_sensor = ColorSensorV3(I2C.Port.kMXP)
            return self.color_sensor.getRawColor()
        else:
            return raw_color