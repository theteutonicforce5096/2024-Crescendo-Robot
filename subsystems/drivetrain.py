from wpimath.geometry import Translation2d, Rotation2d
from wpilib.shuffleboard import Shuffleboard
from wpimath.kinematics import SwerveDrive4Kinematics, ChassisSpeeds
from .swerve_module import SwerveModule
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

        # Max Drivetrain speed
        self.max_drivetrain_speed = 0.5
        self.drivers_tab_speed = Shuffleboard.getTab("Drivers").add(f"Max Swerve Drive Speed", self.max_drivetrain_speed).withSize(2, 2).getEntry()

        # Drivetrain state
        self.drivetrain_state = "Disabled"
        self.drivers_tab_state = Shuffleboard.getTab("Drivers").add(f"Swerve Drive State", self.drivetrain_state).withSize(2, 2).getEntry()

        self.s_widget = Shuffleboard.getTab("PID").add(f"S", 0.0).withSize(2, 2).getEntry()
        self.v_widget = Shuffleboard.getTab("PID").add(f"V", 0.0).withSize(2, 2).getEntry()
        self.a_widget = Shuffleboard.getTab("PID").add(f"A", 0.0).withSize(2, 2).getEntry()
        self.p_widget = Shuffleboard.getTab("PID").add(f"P", 0.0).withSize(2, 2).getEntry()
        self.i_widget = Shuffleboard.getTab("PID").add(f"I", 0.0).withSize(2, 2).getEntry()
        self.d_widget = Shuffleboard.getTab("PID").add(f"D", 0.0).withSize(2, 2).getEntry()
        self.acceleration_widget = Shuffleboard.getTab("PID").add(f"Acceleration", 0.0).withSize(2, 2).getEntry()
        self.jerk_widget = Shuffleboard.getTab("PID").add(f"Jerk", 0.0).withSize(2, 2).getEntry()

    def reset_drivetrain(self):
        """
        Reset Swerve Modules.
        """
        self.front_left_module.reset()
        self.front_right_module.reset()
        self.back_left_module.reset()
        self.back_right_module.reset()

    def set_pid(self):
        self.front_left_module.set_pid(self.s_widget.getFloat(0.0), self.v_widget.getFloat(0.0), self.a_widget.getFloat(0.0), self.p_widget.getFloat(0.0),
                                   self.i_widget.getFloat(0.0), self.d_widget.getFloat(0.0), self.acceleration_widget.getFloat(0.0), self.jerk_widget.getFloat(0.0))
        self.front_right_module.set_pid(self.s_widget.getFloat(0.0), self.v_widget.getFloat(0.0), self.a_widget.getFloat(0.0), self.p_widget.getFloat(0.0),
                                   self.i_widget.getFloat(0.0), self.d_widget.getFloat(0.0), self.acceleration_widget.getFloat(0.0), self.jerk_widget.getFloat(0.0))
        self.back_left_module.set_pid(self.s_widget.getFloat(0.0), self.v_widget.getFloat(0.0), self.a_widget.getFloat(0.0), self.p_widget.getFloat(0.0),
                                   self.i_widget.getFloat(0.0), self.d_widget.getFloat(0.0), self.acceleration_widget.getFloat(0.0), self.jerk_widget.getFloat(0.0))
        self.back_right_module.set_pid(self.s_widget.getFloat(0.0), self.v_widget.getFloat(0.0), self.a_widget.getFloat(0.0), self.p_widget.getFloat(0.0),
                                   self.i_widget.getFloat(0.0), self.d_widget.getFloat(0.0), self.acceleration_widget.getFloat(0.0), self.jerk_widget.getFloat(0.0))

    def reset_gyro(self):
        """
        Reset Gyro.
        """
        self.gyro.reset()
        self.drivers_tab_gyro.setFloat(0)

    def change_max_drivetrain_speed(self, speed):
        """
        Change max drivetrain speed.
        """
        self.max_drivetrain_speed = speed
        self.drivers_tab_speed.setFloat(self.max_drivetrain_speed)

    def change_drivetrain_state(self, state):
        """
        Change the drivetrain's state.
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
        """
        # Get desired Swerve Modules' speeds and angles.
        current_robot_angle = self.get_current_robot_angle()
        self.drivers_tab_gyro.setFloat(round(current_robot_angle, 2))
        robot_speeds = ChassisSpeeds.fromFieldRelativeSpeeds(forward_speed, strafe_speed, rotation_speed, Rotation2d.fromDegrees(current_robot_angle))
        front_left_module_state, front_right_module_state, back_left_module_state, back_right_module_state = self.kinematics.desaturateWheelSpeeds(self.kinematics.toSwerveModuleStates(robot_speeds), self.max_drivetrain_speed * 5.21208)
        
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