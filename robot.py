import wpilib
import wpilib.drive
import os
import ntcore
from cscore import CameraServer
from magicbot import MagicRobot
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from rev import ColorSensorV3
from photonlibpy import photonCamera
import navx
from navx import AHRS

import vision

class MyRobot(MagicRobot):
    def createObjects(self):
        self.joystick = wpilib.Joystick(0)
        pass
    def teleopInit(self):
        self.colorSensor = ColorSensorV3(wpilib.I2C.Port.kMXP)
        self.cam = photonCamera.PhotonCamera('main')

    def teleopPeriodic(self):
        self.proximity = self.colorSensor.getProximity()
        wpilib.SmartDashboard.putNumber("Proximity", self.proximity)
        self.rawDetectColor = self.colorSensor.getRawColor()
        wpilib.SmartDashboard.putNumber("Raw Red", self.rawDetectColor.red)
        wpilib.SmartDashboard.putNumber("Raw Green", self.rawDetectColor.green)
        wpilib.SmartDashboard.putNumber("Raw Blue", self.rawDetectColor.blue)
        self.result = self.cam.getLatestResult()
        if self.result.hasTargets():
            self.targets = self.result.getTargets()
            self.bestTarget = self.result.getBestTarget()
            self.cameraPos = self.bestTarget.getBestCameraToTarget()
            while self.cameraPos.x > 0.5:
                #forward
                pass
            while self.cameraPos.z != 0:
                if self.cameraPos.z > 0:
                    pass
            print(self.cameraPos)
            wpilib.SmartDashboard.putNumberArray("Cam", self.cameraPos)
            wpilib.SmartDashboard.putNumber("X Position (relative to tag)", self.cameraPos.x)
            wpilib.SmartDashboard.putNumber("Y Position (relative to tag)", self.cameraPos.y)
            wpilib.SmartDashboard.putNumber("Z Position (relative to tag)", self.cameraPos.z)
        pass
        self.vision = vision.Vision("main", wpilib.I2C.Port.kOnboard)
        pass

    def teleopPeriodic(self):
        self.vision.updateCameraPosition()
        self.vision.updateColorSensor()
        rotationSpeed = 0
        if self.joystick.getRawButtonPressed(3):
            if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kBlue:
                self.vision.moveToTarget(7)
                self.vision.moveToTarget(8)
            elif wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kRed:
                self.vision.moveToTarget(3)
                self.vision.moveToTarget(4)
        else:
            rotationSpeed = self.joystick.getRawAxis(2)
        iamspeed = self.joystick.getRawAxis(1)
        #send da commands to da drivetrain

    
    def autonomousInit(self):
        pass

    def autonomous(self):
        # For auto, use MagicBot's auto mode.
        # This will load the ./autonomous folder.
        super().autonomous()

if __name__ == '__main__':
    wpilib.run(MyRobot)