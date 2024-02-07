import wpilib
import wpimath.controller
from photonlibpy import photonCamera
from rev import ColorSensorV3


class Vision():
    
    def __init__(self, camera: str, colorSensor: wpilib.I2C.Port):
        """
        Initializer for the Vision module.

        :param camera: Name of the camera. Can be found in the PhotonVision dashboard.
        :type camera: str
        :param colorSensor: Location of the color sensor port on the board.
        :type colorSensor: Port
        """
        self.colorSensor = ColorSensorV3(colorSensor)
        self.cam = photonCamera.PhotonCamera(camera)
        self.rotationPID = wpimath.controller.PIDController(0.0, 0, 0.1)

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

    def updateCameraPosition(self):
        self.cameraPos = self.bestTarget.getBestCameraToTarget()
        wpilib.SmartDashboard.putNumber("X Position (relative to tag)", self.cameraPos.x)
        wpilib.SmartDashboard.putNumber("Y Position (relative to tag)", self.cameraPos.y)
        wpilib.SmartDashboard.putNumber("Z Position (relative to tag)", self.cameraPos.z)

    def moveToTarget(self, target: str):
        """
        Move the robot to a given target.

        :param target: The target to move to. Must be a tag ID.
        :type target: int
        """
        rotationSpeed = 0
        self.result = self.cam.getLatestResult()
        if self.result.hasTargets() == True:
            self.targets = self.result.getTargets()
            self.bestTarget = self.result.getBestTarget()
            self.yaw = self.bestTarget.getYaw()
            wpilib.SmartDashboard.putNumber("Target ID", self.bestTarget.fiducialId)
            if self.bestTarget.fiducialId == target:
                wpilib.SmartDashboard.putBoolean("Target Found (last press)", True)
                return self.rotationPID.calculate(self.yaw)
            else:
                wpilib.SmartDashboard.putBoolean("Target Found (last press)", False)
                return 0
