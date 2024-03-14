from photonlibpy import photonCamera, photonUtils
from math import radians
from wpilib.shuffleboard import Shuffleboard 
from wpilib import DriverStation

class Vision():
    def __init__(self):
        """
        Initializer for the Vision module.

        :param camera: Name of the camera. Can be found in the PhotonVision dashboard.
        :type camera: str
        """
        self.camera = photonCamera.PhotonCamera('main')
        self.speaker_distance = Shuffleboard.getTab("Drivers").add(f"Distance to Speaker", "None").withSize(2, 2).getEntry()
        
        # if DriverStation.getAlliance() == DriverStation.Alliance.kBlue:
        #     self.tag = 7
        # else:
        #     self.tag = 4

        self.tag = 6

        self.camera_height = 0.43815
        self.target_height = 1.431925
        self.camera_pitch = radians(32)

    def reset(self):
        self.speaker_distance.setString("None")
        
        # if DriverStation.getAlliance() == DriverStation.Alliance.kBlue:
        #     self.tag = 7
        # else:
        #     self.tag = 4

        self.tag = 6

    def get_data_to_speaker(self):
        result = self.camera.getLatestResult()
        if result.hasTargets() == True:
            targets = result.getTargets()
            for target in targets:
                if target.getFiducialId() == self.tag:
                    distance = photonUtils.PhotonUtils.calculateDistanceToTargetMeters(self.camera_height, self.target_height, self.camera_pitch, (radians(target.getPitch())))
                    yaw = target.getYaw()
                    self.speaker_distance.setString(str(distance))
                    return distance, yaw
                else:
                    self.speaker_distance.setString("Can't find AprilTag.")

        return None, None