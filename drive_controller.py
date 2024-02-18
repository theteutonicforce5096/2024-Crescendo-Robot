import wpilib
import wpimath
import robot
import math
from photonlibpy import photonCamera, photonUtils

class DriveController():
    def __init__(self):
        self.frontCam = photonCamera.PhotonCamera('frontCamera')
        self.backCam = photonCamera.PhotonCamera('backCamera')
        self.rotationPID = wpimath.controller.PIDController(0.0, 0, 0.1)
        self.movementPID = wpimath.controller.PIDController(0.1, 0, 0.0)

    def alignToSpeaker(self):
        if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kBlue:
            tag = 7
        else:
            tag = 4
        self.result = self.frontCam.getLatestResult()
        if self.result.hasTargets() == True:
            self.targets = self.result.getTargets()
            self.bestTarget = self.result.getBestTarget()
            self.yaw = self.bestTarget.getYaw()
            wpilib.SmartDashboard.putNumber("Target ID", self.bestTarget.fiducialId)
            if self.bestTarget.fiducialId == tag:
                rotationSpeed = self.rotationPID.calculate(self.yaw, 0)
                if not rotationSpeed:
                    rotationSpeed = 0.0
            else:
                rotationSpeed = 0.0
        else:
            rotationSpeed = 0.0
        return rotationSpeed
    
    def alignToAmp(self):
        if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kBlue:
            tag = 6
        else:
            tag = 5
        self.result = self.frontCam.getLatestResult()
        if self.result.hasTargets() == True:
            self.targets = self.result.getTargets()
            self.bestTarget = self.result.getBestTarget()
            self.pose = wpimath.objectToRobotPose(self.bestTarget)
            self.yaw = self.bestTarget.getYaw()
            wpilib.SmartDashboard.putNumber("Target ID", self.bestTarget.fiducialId)
            frontCameraHeightMeters = 0
            targetHeightMeters = 0
            frontCameraPitch = math.radians(0)
            if self.bestTarget.fiducialId == tag:
                rotationSpeed = self.rotationPID.calculate(self.yaw, 0)
                range = photonUtils.PhotonUtils.calculateDistanceToTargetMeters(frontCameraHeightMeters, targetHeightMeters, frontCameraPitch, (math.radians(self.bestTarget.getPitch())))
                forwardSpeed = self.movementPID.calculate(range, 0.5)
                if not forwardSpeed and not rotationSpeed:
                    rotationSpeed = 0.0
                    forwardSpeed = 0.0
            else:
                rotationSpeed = 0.0
                forwardSpeed = 0.0
        else:
            rotationSpeed = 0.0
            forwardSpeed = 0.0
        return [forwardSpeed, rotationSpeed]
    # def alignToLoadingStation(self):
    #     if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kBlue:
    #         tag = 2
    #     else:
    #         tag = 10
    #     self.result = self.frontCam.getLatestResult()
    #     if self.result.hasTargets() == True:
    #         self.targets = self.result.getTargets()
    #         self.bestTarget = self.result.getBestTarget()
    #         self.yaw = self.bestTarget.getYaw()
    #         wpilib.SmartDashboard.putNumber("Target ID", self.bestTarget.fiducialId)
    #         if self.bestTarget.fiducialId == tag:
    #             rotationSpeed = self.rotationPID.calculate(self.yaw, 0)
    #             if not rotationSpeed:
    #                 rotationSpeed = 0.0
    #         else:
    #             rotationSpeed = 0.0
    #     else:
    #         rotationSpeed = 0.0
    #     return rotationSpeed