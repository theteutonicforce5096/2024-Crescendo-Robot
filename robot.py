import wpilib
import wpilib.drive
import os
import ntcore
from cscore import CameraServer
from magicbot import MagicRobot
from robotpy_ext.autonomous.selector import AutonomousModeSelector
import autonomous
import cv2
import subsystems.vision
from rev import ColorSensorV3

class MyRobot(MagicRobot):
    # subsystems.vision.Vision()
    def createObjects(self):
        self.joystick = wpilib.Joystick(0)
        pass
    def teleopInit(self):
        self.ColorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)

    def teleopPeriodic(self):
        self.joystick
        proximity = self.ColorSensor.getProximity()
        wpilib.SmartDashboard.putNumber("Proximity", proximity)
        rawDetectColor = self.ColorSensor.getRawColor()
        wpilib.SmartDashboard.putNumber("Raw Red", rawDetectColor.Red)
        wpilib.SmartDashboard.putNumber("Raw Green", rawDetectColor.Green)
        wpilib.SmartDashboard.putNumber("Raw Blue", rawDetectColor.Blue)
    
    def autonomousInit(self):
        pass

    def autonomous(self):
        # For auto, use MagicBot's auto mode.
        # This will load the ./autonomous folder.
        super().autonomous()

if __name__ == '__main__':
    wpilib.run(MyRobot)