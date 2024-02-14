import wpilib
import wpilib.drive
import wpimath
import os
import ntcore
from cscore import CameraServer
from magicbot import MagicRobot
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from rev import ColorSensorV3
from photonlibpy import photonCamera
import navx
from navx import AHRS
import pyfrc.physics.drivetrains
import vision
import subsystems.shooter

class MyRobot(MagicRobot):
    def createObjects(self):
        self.joystick = wpilib.Joystick(0)
        pass
    def teleopInit(self):
        self.vision = vision.Vision("main", wpilib.I2C.Port.kMXP)
        self.controller = wpilib.XboxController(0)

    # def teleopPeriodic(self):
    #     self.proximity = self.colorSensor.getProximity()
    #     wpilib.SmartDashboard.putNumber("Proximity", self.proximity)
    #     self.rawDetectColor = self.colorSensor.getRawColor()
    #     wpilib.SmartDashboard.putNumber("Raw Red", self.rawDetectColor.red)
    #     wpilib.SmartDashboard.putNumber("Raw Green", self.rawDetectColor.green)
    #     wpilib.SmartDashboard.putNumber("Raw Blue", self.rawDetectColor.blue)
    #     self.result = self.cam.getLatestResult()
    #     if self.result.hasTargets():
    #         self.targets = self.result.getTargets()
    #         self.bestTarget = self.result.getBestTarget()
    #         self.cameraPos = self.bestTarget.getBestCameraToTarget()
    #         while self.cameraPos.x > 0.5:
    #             #forward
    #             pass
    #         while self.cameraPos.z != 0:
    #             if self.cameraPos.z > 0:
    #                 pass
    #         print(self.cameraPos)
    #         wpilib.SmartDashboard.putNumberArray("Cam", self.cameraPos)
    #         wpilib.SmartDashboard.putNumber("X Position (relative to tag)", self.cameraPos.x)
    #         wpilib.SmartDashboard.putNumber("Y Position (relative to tag)", self.cameraPos.y)
    #         wpilib.SmartDashboard.putNumber("Z Position (relative to tag)", self.cameraPos.z)
    #     pass
    #     self.vision = vision.Vision("main", wpilib.I2C.Port.kOnboard)
    #     pass

    def teleopPeriodic(self):
        self.vision.updateCameraPosition()
        self.vision.updateColorSensor()
        rotationSpeed = 0
        forwardSpeed = 0
        # if self.joystick.getRawButtonPressed(3):
        #     if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kBlue:
        #         forwardSpeed, rotationSpeed = self.vision.moveToTarget(7)
        #         forwardSpeed, rotationSpeed = self.vision.moveToTarget(8)
        #     elif wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kRed:
        #         forwardSpeed, rotationSpeed = self.vision.moveToTarget(3)
        #         forwardSpeed, rotationSpeed = self.vision.moveToTarget(4)
        # else:
        #     rotationSpeed = self.joystick.getRawAxis(2)
        #     forwardSpeed = self.joystick.getRawAxis(1)
        forwardSpeed, rotationSpeed = self.vision.moveToTarget(3)
        print(f"forwardSpeed: {forwardSpeed}\nrotationSpeed: {rotationSpeed}")
        wpilib.SmartDashboard.putNumber("forwardSpeed", forwardSpeed)
        wpilib.SmartDashboard.putNumber("rotationSpeed", rotationSpeed)
        #send da commands to da drivetrain
        
        if joystick.getRawButton(5):
            turnIntakeOn()
        else:
            turnIntakeOff()

    def autonomousInit(self):
        pass

    def autonomous(self):
        # For auto, use MagicBot's auto mode.
        # This will load the ./autonomous folder.
        super().autonomous()

if __name__ == '__main__':
    wpilib.run(MyRobot)