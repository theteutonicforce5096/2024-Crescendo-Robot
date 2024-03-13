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
        # TODO: Recommend you pass in the DIO port number to this constructor. It keeps things consistent with other subsystem modules, and it makes it much easier if we ever end up having multiple such sensors around the robot.
        #self.photoelectric_sensor = DigitalOutput(1)
        # TODO: From the point-of-view of the RoboRIO, the sensor is a digital input, not an output.
        self.dio_entry = Shuffleboard.getTab("Drivers").add(f"Ring Detected (Photoelectric Sensor)", "None").withSize(2, 2).getEntry()

    def reset(self):
        self.dio_entry.setString("False")
        # TODO: What is the purpose of this reset() method? It  doesn't do anything with the sensor.
    
    def detects_ring(self):
        """
        Check for a ring in the robot.
        """
        # if self.photoelectric_sensor.get() == False:
        #     self.dio_entry.setString("True")
        #     return True
        # else:
        #     self.dio_entry.setString("False")
        #     return False
        return False