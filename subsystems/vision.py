from photonlibpy import photonCamera, photonUtils
from math import radians
from wpilib.shuffleboard import Shuffleboard 

class Vision():
    def __init__(self, inBackCamera: str):
        """
        Initializer for the Vision module.

        :param camera: Name of the camera. Can be found in the PhotonVision dashboard.
        :type camera: str
        """
        self.backCamera = photonCamera(inBackCamera)
        self.backCam = photonCamera.PhotonCamera('backCamera')
        self.speaker_distance = Shuffleboard.getTab("Drivers").add(f"Speaker Distance", 0.0).getEntry()
            
    def get_distance_to_speaker(self):
        cameraHeightMeters = 0
        targetHeightMeters = 0
        cameraPitch = radians(0)

        self.bestTarget = self.backCam.getLatestResult().getBestTarget()
        
        distance = photonUtils.PhotonUtils.calculateDistanceToTargetMeters(cameraHeightMeters, targetHeightMeters, cameraPitch, (radians(self.bestTarget.getPitch())))
        self.speaker_distance.setFloat(distance)