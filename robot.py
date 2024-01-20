import wpilib
import wpilib.drive
import ctre
import os
import ntcore
import robotpy_apriltag
from cscore import CameraServer
from magicbot import MagicRobot
from robotpy_ext.autonomous.selector import AutonomousModeSelector
import autonomous
from rev.color import ColorSensorV3

class MyRobot(MagicRobot):

    def createObjects(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        rev.color.ColorSensorV3
    
    def autonomousInit(self):
        pass

    def autonomous(self):
        # For auto, use MagicBot's auto mode.
        # This will load the ./autonomous folder.
        super().autonomous()

if __name__ == '__main__':
    wpilib.run(MyRobot)