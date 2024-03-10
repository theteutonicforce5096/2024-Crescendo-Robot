from wpilib import DigitalOutput 
from wpilib.shuffleboard import Shuffleboard

class PhotoelectricSensor():
    """
    Class for using photoelectric sensor on robot.
    """
    
    def __init__(self):
        """
        Constructor for photoelectric sensor.
        """
        self.photoelectric_sensor = DigitalOutput(0)
        self.dio_entry = Shuffleboard.getTab("Drivers").add(f"Ring Detected (Photoelectric Sensor)", "None").withSize(2, 2).getEntry()

    def reset(self):
        self.dio_entry.setString("False")
    
    def detects_ring(self):
        """
        Check for a ring in the robot.
        """
        if self.photoelectric_sensor.get() == False:
            self.dio_entry.setString("True")
            return True
        else:
            self.dio_entry.setString("False")
            return False