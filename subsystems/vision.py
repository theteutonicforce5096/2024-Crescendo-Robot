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
        #self.backCamera = photonCamera('main'))
        self.camera = photonCamera.PhotonCamera('main')
        self.speaker_distance = Shuffleboard.getTab("Drivers").add(f"Distance to Speaker", "None").withSize(2, 2).getEntry()
        self.speaker_angle = Shuffleboard.getTab("Drivers").add(f"Angle to Speaker", "None").withSize(2, 2).getEntry()
        
        if DriverStation.getAlliance() == DriverStation.Alliance.kBlue:
            self.tag = 7
        else:
            self.tag = 4

    def reset(self):
        self.speaker_distance = Shuffleboard.getTab("Drivers").add(f"Distance to Speaker", "None").withSize(2, 2).getEntry()
        self.speaker_angle = Shuffleboard.getTab("Drivers").add(f"Angle to Speaker", "None").withSize(2, 2).getEntry()
        
        if DriverStation.getAlliance() == DriverStation.Alliance.kBlue:
            self.tag = 7
        else:
            self.tag = 4

    def get_distance_to_speaker(self):
        cameraHeightMeters = 0.43815
        targetHeightMeters = 1.431925
        cameraPitch = radians(33)

        result = self.camera.getLatestResult()
        print("I am here")
        if result.hasTargets() == True:
            targets = result.getTargets()
            for target in targets:
                print("Scanning")
                if target.getFiducialId() == self.tag:
                    print("Found")
                    distance = photonUtils.PhotonUtils.calculateDistanceToTargetMeters(cameraHeightMeters, targetHeightMeters, cameraPitch, (radians(target.getPitch())))
                    self.speaker_distance.setString(str(distance))
                    self.speaker_angle.setString(str(target.getYaw()))
                    print(target.getPitch())
                else:
                    self.speaker_distance.setString("None")
                    self.speaker_angle.setString("None")