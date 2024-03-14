from wpilib import DigitalInput 
from wpilib.shuffleboard import Shuffleboard

class PhotoelectricSensor():
    """
    Class for using photoelectric sensor on robot.
    """
    
    def __init__(self, channel):
        """
        Constructor for photoelectric sensor.
        """
        self.photoelectric_sensor = DigitalInput(channel)
        self.ring_entry = Shuffleboard.getTab("Drivers").add(f"Ring Detected", "None").withSize(2, 2).getEntry()
    
    def detects_ring(self):
        """
        Check for a ring in the robot.
        """
        if self.photoelectric_sensor.get() == False:
            self.ring_entry.setString("True")
            return True
        else:
            self.ring_entry.setString("False")
            return False