from photonlibpy import photonCamera
from math import radians, sin
from wpilib.shuffleboard import Shuffleboard 
from wpimath.controller import PIDController

class Vision():
    def __init__(self):
        """
        Initializer for the Vision module.

        :param camera: Name of the camera. Can be found in the PhotonVision dashboard.
        :type camera: str
        """
        self.camera = photonCamera.PhotonCamera('main')
        self.tag_distance = Shuffleboard.getTab("AprilTags").add(f"Distance to AprilTag", "None").withSize(2, 2).getEntry()
        self.tag_yaw = Shuffleboard.getTab("AprilTags").add(f"Yaw to AprilTag", "None").withSize(2, 2).getEntry()
        self.tag = 7

        self.camera_height = 0.43815
        self.target_height = 1.431925
        self.camera_pitch = radians(30)
        
        self.controller = PIDController(1)
        self.controller.setTolerance(0.5)

    def reset(self):
        self.controller.reset()
        self.tag_distance.setString("None")
        self.tag_yaw.setString("None")
        self.tag = 7

    def update(self):
        result = self.camera.getLatestResult()
        if result.targets:
            targets = result.getTargets()
            for target in targets:
                if target.getFiducialId() == self.tag:
                    distance = (self.target_height - self.camera_height) / sin(self.camera_pitch + radians(target.getPitch()))
                    yaw = target.getYaw()

                    self.tag_distance.setString(str(distance))
                    self.tag_yaw.setString(str(yaw))
                    return self.tag_yaw
        else:
            self.tag_distance.setString("Can't find AprilTag.")
            self.tag_yaw.setString("Can't find AprilTag.")


    def align_to_target(self):
        self.controller.reset()
        self.controller.setSetpoint(0)

    def update_vision_controller(self, value):
        if self.controller.atSetpoint():
            return "Done"
        
        return self.controller.calculate(value)