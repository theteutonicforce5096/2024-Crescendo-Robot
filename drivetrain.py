from wpimath.geometry import Translation2d, Rotation2d
from wpilib.shuffleboard import Shuffleboard
from wpimath.kinematics import SwerveDrive4Kinematics, ChassisSpeeds
from swerve_module import SwerveModule
from wpilib import XboxController, Timer
import navx 

class SwerveDrive():
    """Class for controlling Swerve Drive on robot."""

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
        self.front_left_module = SwerveModule("FL", 23, 13, 33, "CANivore", "CANivore", "rio", -0.007080, False)
        self.front_right_module = SwerveModule("FR", 20, 10, 30, "CANivore", "CANivore", "rio", 0.006104, True)
        self.back_left_module = SwerveModule("BL", 22, 12, 32, "CANivore", "CANivore", "rio", -0.475830, False)
        self.back_right_module = SwerveModule("BR", 21, 11, 31, "CANivore", "CANivore", "rio", -0.007080, True)

        # Initialize Gyro
        self.gyro = navx.AHRS.create_spi()
        self.drivers_tab_gyro = Shuffleboard.getTab("Drivers").add(f"Current Robot Angle (From Gyro)", round(self.get_current_robot_angle(), 2)).withSize(2, 2).getEntry()

        # Initialize drivetrain controller
        self.drivetrain_controller = XboxController(0)

        # Initialize timer
        self.drivetrain_timer = Timer()

        # Set default robot speeds
        self.forward_speed = 0
        self.strafe_speed = 0
        self.rotation_speed = 0

        # Max Drivetrain speed
        self.max_drivetrain_speed = 0.5
        self.drivers_tab_speed = Shuffleboard.getTab("Drivers").add(f"Max Swerve Drive Speed", self.max_drivetrain_speed).withSize(2, 2).getEntry()

        # Drivetrain state
        self.drivetrain_state = "Disabled"
        self.drivers_tab_state = Shuffleboard.getTab("Drivers").add(f"Swerve Drive State", self.drivetrain_state).withSize(2, 2).getEntry()

    def reset_timer(self):
        """
        Reset drivetrain timer.
        """
        self.drivetrain_timer.reset()

    def reset_robot_speeds(self):
        """
        Reset robot speeds.
        """
        self.forward_speed = 0
        self.strafe_speed = 0
        self.rotation_speed = 0

    def reset_drivetrain(self):
        """
        Reset Swerve Modules.
        """
        self.front_left_module.reset()
        self.front_right_module.reset()
        self.back_left_module.reset()
        self.back_right_module.reset()

    def reset_gyro(self):
        """
        Reset Gyro.
        """
        self.gyro.reset()
        self.drivers_tab_gyro.setFloat(0)

    def change_max_drivetrain_speed(self, speed):
        """
        Change max drivetrain speed.

        :param speed: Max speed of the drivetrain
        :type speed: float
        """
        self.max_drivetrain_speed = speed
        self.drivers_tab_speed.setFloat(self.max_drivetrain_speed)

    def change_drivetrain_state(self, state):
        """
        Change the drivetrain's state.

        :param state: State of the drivetrain
        :type state: str
        """
        self.drivetrain_state = state
        self.drivers_tab_state.setString(self.drivetrain_state)

    def get_drivetrain_state(self):
        """
        Get the drivetrain's state.
        """
        return self.drivetrain_state

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

    def move_robot(self, forward_speed, strafe_speed, rotation_speed):
        """
        Move the robot by a forward speed, strafe speed, and rotation speed.

        :param forward_speed: Desired forward speed of the robot
        :type forward_speed: float
        :param strafe_speed: Desired strafe speed of the robot.
        :type strafe_speed: float
        :param rotation_speed: Desired rotation speed of the robot.
        :type rotation_speed: float
        """
        # Get desired Swerve Modules' speeds and angles.
        current_robot_angle = self.get_current_robot_angle()
        self.drivers_tab_gyro.setFloat(round(current_robot_angle, 2))
        robot_speeds = ChassisSpeeds.fromFieldRelativeSpeeds(forward_speed, strafe_speed, rotation_speed, Rotation2d.fromDegrees(current_robot_angle))
        front_left_module_state, front_right_module_state, back_left_module_state, back_right_module_state = self.kinematics.desaturateWheelSpeeds(self.kinematics.toSwerveModuleStates(robot_speeds), self.max_drivetrain_speed)
        
        # Optimize desired Swerve Modules' angles.
        front_left_module_state = front_left_module_state.optimize(front_left_module_state, self.front_left_module.current_angle)
        front_right_module_state = front_right_module_state.optimize(front_right_module_state, self.front_right_module.current_angle)
        back_left_module_state = back_left_module_state.optimize(back_left_module_state, self.back_left_module.current_angle)
        back_right_module_state = back_right_module_state.optimize(back_right_module_state, self.back_right_module.current_angle)

        # Set the Swerve Modules to the desired speeds and angles.
        self.front_left_module.set(front_left_module_state.speed, front_left_module_state.angle)
        self.front_right_module.set(front_right_module_state.speed, front_right_module_state.angle)
        self.back_left_module.set(back_left_module_state.speed, back_left_module_state.angle)
        self.back_right_module.set(back_right_module_state.speed, back_right_module_state.angle)

    def stop_robot(self):
        """
        Stop moving the robot and hold its current position.
        """
        # Stop all of the Swerve Modules. 
        self.front_left_module.stop()
        self.front_right_module.stop()
        self.back_left_module.stop()
        self.back_right_module.stop()

    def _check_for_gyro_reset(self):
        """
        Check if gyro needs to be reset.
        """
        if self.drivetrain_controller.getAButtonPressed():
            self.stop_robot()
            self.reset_gyro()
            self.drivetrain_timer.restart()
            self.change_drivetrain_state("Disabled")

    def _check_for_max_drivetrain_speed_change(self):
        """
        Check if max drivetrain speed needs to be changed.
        """
        if (self.drivetrain_controller.getLeftTriggerAxis() > 0.1) != (self.drivetrain_controller.getRightTriggerAxis() > 0.1):
            self.change_max_drivetrain_speed(0.75)
        elif self.drivetrain_controller.getLeftTriggerAxis() > 0.1 and self.drivetrain_controller.getRightTriggerAxis() > 0.1:
            self.change_max_drivetrain_speed(1.0)
        else:
            self.change_max_drivetrain_speed(0.5)

    def _check_for_deadzone(self, forward_speed, strafe_speed, rotation_speed):
        """
        Check for deadzone on forward speed, strafe speed, and rotation speed.

        :param forward_speed: Desired forward speed of the robot
        :type forward_speed: float
        :param strafe_speed: Desired strafe speed of the robot.
        :type strafe_speed: float
        :param rotation_speed: Desired rotation speed of the robot.
        :type rotation_speed: float
        """
        # Set deadzone on forward speed.
        if forward_speed > 0.1 or forward_speed < -0.1:
            self.forward_speed = forward_speed
        else:
            self.forward_speed = 0

        # Set deadzone on strafe speed.
        if strafe_speed > 0.1 or strafe_speed < -0.1:
            self.strafe_speed = strafe_speed
        else:
            self.strafe_speed = 0

        # Set deadzone on rotation speed.
        if rotation_speed > 0.1 or rotation_speed < -0.1:
            self.rotation_speed = rotation_speed
        else:
            self.rotation_speed = 0

    def _set_controller_rumble(self, rumble):
        """
        Set the rumble of the drivetrain controller.

        :param rumble: Rumble of the controller
        :type rumble: float
        """
        self.drivetrain_controller.setRumble(XboxController.RumbleType.kBothRumble, rumble)  

    def update_robot_position(self):
        """
        Update position of the robot from controller commands.
        """ 
        # Get speeds from drivetrain controller.
        forward_speed = self.drivetrain_controller.getLeftY()
        strafe_speed = self.drivetrain_controller.getLeftX()
        rotation_speed = self.drivetrain_controller.getRightX()

        self._check_for_gyro_reset()
        self._check_for_max_drivetrain_speed_change()
        self._check_for_deadzone(forward_speed, strafe_speed, rotation_speed)

        # Move robot if drivetrain is enabled.
        match self.get_drivetrain_state():
            case "Enabled":
                if self.forward_speed != 0 or self.strafe_speed != 0 or self.rotation_speed != 0:
                    self.move_robot(self.forward_speed, self.strafe_speed, self.rotation_speed) 
                else:
                    self.stop_robot()
            case "Disabled":
                if not self.drivetrain_timer.hasElapsed(0.5):
                    if self.forward_speed != 0 or self.strafe_speed != 0 or self.rotation_speed != 0:
                        self._set_controller_rumble(0.75)  
                    else:
                        self._set_controller_rumble(0)  
                else:
                    self._set_controller_rumble(0)  
                    self.reset_timer()
                    self.change_drivetrain_state("Enabled")
        