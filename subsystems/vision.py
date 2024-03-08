from photonlibpy import photonCamera, photonUtils
from math import radians
from wpilib.shuffleboard import Shuffleboard 
from wpilib import DriverStation

class Vision():
    def __init__(self, inBackCamera: str):
        """
        Initializer for the Vision module.

        :param camera: Name of the camera. Can be found in the PhotonVision dashboard.
        :type camera: str
        """
        self.backCamera = photonCamera(inBackCamera)
        self.backCam = photonCamera.PhotonCamera('backCamera')
        self.speaker_distance = Shuffleboard.getTab("Drivers").add(f"Distance to Speaker", "None").getEntry()
        
        if DriverStation.getAlliance() == DriverStation.Alliance.kBlue:
            self.tag = 7
        else:
            self.tag = 4
            
    def get_distance_to_speaker(self):
        cameraHeightMeters = 0
        targetHeightMeters = 1.431925
        cameraPitch = radians(0)

        self.bestTarget = self.backCam.getLatestResult().getBestTarget()

        if self.bestTarget.getFiducialId() == self.tag:
            distance = photonUtils.PhotonUtils.calculateDistanceToTargetMeters(cameraHeightMeters, targetHeightMeters, cameraPitch, (radians(self.bestTarget.getPitch())))
            self.speaker_distance.setString(str(distance))