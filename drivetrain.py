from wpimath.geometry import Translation2d, Rotation2d
from wpimath.kinematics import SwerveDrive4Kinematics, ChassisSpeeds
from swerve_module import SwerveModule
import navx
    
class SwerveDrive():
    """Class for controlling swerve drive on robot."""

    def __init__(self):
        """
        Constructor for Swerve Drive.
        """        
        # Locations of Swerve Modules.
        front_left_location = Translation2d(0.250825, 0.250825)
        front_right_location = Translation2d(0.250825, -0.250825)
        back_left_location = Translation2d(-0.250825, 0.250825)
        back_right_location = Translation2d(-0.250825, -0.250825)

        # Create Kinematics object and initialize Swerve Modules
        self.kinematics = SwerveDrive4Kinematics(front_left_location, front_right_location, back_left_location, back_right_location)
        self.front_left_module = SwerveModule("FL", 23, 13, 33, "CANivore", "CANivore", "rio", -0.002686, False)
        self.front_right_module = SwerveModule("FR", 20, 10, 30, "CANivore", "CANivore", "rio", 0.003906, True)
        self.back_left_module = SwerveModule("BL", 22, 12, 32, "CANivore", "CANivore", "rio", -0.476807, False)
        self.back_right_module = SwerveModule("BR", 21, 11, 31, "CANivore", "CANivore", "rio", 0.002930, True)

        # Initialize Gyro
        self.gyro = navx.AHRS.create_spi()

    def reset(self):
        """
        Reset Swerve Modules and Gyro.
        """
        self.front_left_module.reset()
        self.front_right_module.reset()
        self.back_left_module.reset()
        self.back_right_module.reset()
        self.gyro.reset()

    def get_current_robot_angle(self):
        """
        Get the current robot angle relative to the field using the gyro.
        """
        # Scale the gyro angle from -360 to 360 scale to -180 to 180 scale.
        current_robot_angle = (self.gyro.getAngle() * -1) % 360
        if current_robot_angle > 180: 
            current_robot_angle -= 360
        elif current_robot_angle < -180:
            current_robot_angle += 360

        return current_robot_angle

    def move_robot(self, forward_speed, stafe_speed, rotation_speed):
        """
        Move the robot by a forward speed, strafe speed, and rotation speed.
        """
        # Get desired Swerve Modules' speeds and angles.
        current_robot_angle = self.get_current_robot_angle()
        robot_speeds = ChassisSpeeds.fromFieldRelativeSpeeds(stafe_speed, forward_speed, rotation_speed, Rotation2d.fromDegrees(current_robot_angle))
        front_left_module_state, front_right_module_state, back_left_module_state, back_right_module_state = self.kinematics.desaturateWheelSpeeds(self.kinematics.toSwerveModuleStates(robot_speeds), 1)
        
        # Optimize desired Swerve Modules' angles.
        front_left_module_state = front_left_module_state.optimize(front_left_module_state, self.front_left_module.current_angle)
        front_right_module_state = front_right_module_state.optimize(front_right_module_state, self.front_right_module.current_angle)
        back_left_module_state = back_left_module_state.optimize(back_left_module_state, self.back_left_module.current_angle)
        back_right_module_state = back_right_module_state.optimize(back_right_module_state, self.back_right_module.current_angle)

        # Set the Swerve Modules to the desired speeds and angles.
        self.front_left_module.set(front_left_module_state.speed * 0.75, front_left_module_state.angle)
        self.front_right_module.set(front_right_module_state.speed * 0.75, front_right_module_state.angle)
        self.back_left_module.set(back_left_module_state.speed * 0.75, back_left_module_state.angle)
        self.back_right_module.set(back_right_module_state.speed * 0.75, back_right_module_state.angle)

    def stop_robot(self):
        """
        Stop moving the robot and hold its current position.
        """
        # Stop all of the Swerve Modules. 
        self.front_left_module.stop()
        self.front_right_module.stop()
        self.back_left_module.stop()
        self.back_right_module.stop()