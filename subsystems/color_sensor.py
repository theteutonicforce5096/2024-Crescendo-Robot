from rev import ColorSensorV3
from wpilib import I2C 
from wpilib.shuffleboard import Shuffleboard

class ColorSensor():
    """Class for using color sensor on robot."""
    
    def __init__(self):
        """
        Constructor for Color Sensor.
        """
        self.color_sensor = ColorSensorV3(I2C.Port.kMXP)
        self.rgb_entry = Shuffleboard.getTab("ColorSensor").add(f"Proximity", "None").withSize(2, 2).getEntry()
    
    def detects_ring(self):
        """
        Check for a ring in the robot.
        """
        self._check_if_disconnected() 
        distance = self.color_sensor.getProximity()
        self.rgb_entry.setString(f"{distance}") 
        if distance > 1500:
            return True
        else:
            return False
        
    def _check_if_disconnected(self):
        if not self.color_sensor.isConnected():
            self.color_sensor = ColorSensorV3(I2C.Port.kMXP)