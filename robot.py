import wpilib
import wpilib.drive
import os
import ntcore
from cscore import CameraServer
from magicbot import MagicRobot
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from rev import ColorSensorV3
from photonlibpy import photonCamera

class MyRobot(MagicRobot):
    # subsystems.vision.Vision()
    def createObjects(self):
        self.joystick = wpilib.Joystick(0)
        pass
    def teleopInit(self):
        # self.colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)
        self.cam = photonCamera.PhotonCamera('main')

    def teleopPeriodic(self):
        # self.proximity = self.colorSensor.getProximity()
        # wpilib.SmartDashboard.putNumber("Proximity", self.proximity)
        # self.rawDetectColor = self.colorSensor.getRawColor()
        # wpilib.SmartDashboard.putNumber("Raw Red", self.rawDetectColor.red)
        # wpilib.SmartDashboard.putNumber("Raw Green", self.rawDetectColor.green)
        # wpilib.SmartDashboard.putNumber("Raw Blue", self.rawDetectColor.blue)
        self.result = self.cam.getLatestResult()
        self.targets = self.result.getTargets()
        self.bestTarget = self.result.getBestTarget()
        print(self.bestTarget)
        # targetvalue = self.ca
        pass
    
    def autonomousInit(self):
        pass

    def autonomous(self):
        # For auto, use MagicBot's auto mode.
        # This will load the ./autonomous folder.
        super().autonomous()

if __name__ == '__main__':
    wpilib.run(MyRobot)