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