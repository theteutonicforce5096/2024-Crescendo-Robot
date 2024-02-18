import wpilib
import wpimath.controller
from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.photonUtils import PhotonUtils
from rev import ColorSensorV3
import math

class Vision():
    
    def __init__(self, inFrontCamera: str, inBackCamera: str, colorSensor: wpilib.I2C.Port):
        """
        Initializer for the Vision module.

        :param camera: Name of the camera. Can be found in the PhotonVision dashboard.
        :type camera: str
        :param colorSensor: Location of the color sensor port on the board.
        :type colorSensor: Port
        """
        self.colorSensor = ColorSensorV3(colorSensor)
        self.frontCamera = PhotonCamera(inFrontCamera)
        self.backCamera = PhotonCamera(inBackCamera)
        self.rotationPID = wpimath.controller.PIDController(0.0, 0, 0.1)
        self.movementPID = wpimath.controller.PIDController(0.1, 0, 0.0)

    def updateColorSensor(self):
        """
        Update the color sensor defined in the initialization.
        """
        self.proximity = self.colorSensor.getProximity()
        wpilib.SmartDashboard.putNumber("Proximity", self.proximity)
        self.rawDetectColor = self.colorSensor.getRawColor()
        wpilib.SmartDashboard.putNumber("Raw Red", self.rawDetectColor.red)
        wpilib.SmartDashboard.putNumber("Raw Green", self.rawDetectColor.green)
        wpilib.SmartDashboard.putNumber("Raw Blue", self.rawDetectColor.blue)

    def hasRing(self) -> bool:
        """
        Check for a ring in the robot.
        """
        self.rawDetectColor = self.colorSensor.getRawColor()
        if self.rawDetectColor.red > 50 and self.rawDetectColor.green > 50 and self.rawDetectColor.blue > 50:
            return True
        else:
            return False

    def updateCameraPosition(self):
        self.result = self.cam.getLatestResult()
        if self.result.hasTargets() == True:
            self.targets = self.result.getTargets()
            self.bestTarget = self.result.getBestTarget()
            self.cameraPos = self.bestTarget.getBestCameraToTarget()
            wpilib.SmartDashboard.putNumber("X Position (relative to tag)", self.cameraPos.x)
            wpilib.SmartDashboard.putNumber("Y Position (relative to tag)", self.cameraPos.y)
            wpilib.SmartDashboard.putNumber("Z Position (relative to tag)", self.cameraPos.z)

    def moveToTarget(self, target: int):
        """
        Move the robot to a given target.

        :param target: The target to move to. Must be a tag ID.
        :type target: int
        """
        rotationSpeed = 0
        self.result = self.cam.getLatestResult()
        # if self.result.hasTargets() == True:
        #     self.targets = self.result.getTargets()
        #     self.bestTarget = self.result.getBestTarget()
        #     self.pose = wpimath.objectToRobotPose(self.bestTarget)
        #     self.yaw = self.bestTarget.getYaw()
        #     wpilib.SmartDashboard.putNumber("Target ID", self.bestTarget.fiducialId)
        #     cameraHeightMeters = 0
        #     targetHeightMeters = 0
        #     cameraPitch = math.radians(0)
        #     if self.bestTarget.fiducialId == target:
        #         rotationSpeed = self.rotationPID.calculate(self.yaw, 0)
        #         range = photonUtils.PhotonUtils.calculateDistanceToTargetMeters(cameraHeightMeters, targetHeightMeters, cameraPitch, (math.radians(self.bestTarget.getPitch())))
        #         forwardSpeed = self.movementPID.calculate(range, 0.5)
        #         if not forwardSpeed and not rotationSpeed:
        #             rotationSpeed = 0.0
        #             forwardSpeed = 0.0
        #     else:
        #         rotationSpeed = 0.0
        #         forwardSpeed = 0.0
        # else:
        #     rotationSpeed = 0.0
        #     forwardSpeed = 0.0
        # return [forwardSpeed, rotationSpeed]
            
