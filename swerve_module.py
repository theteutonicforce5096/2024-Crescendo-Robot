import phoenix6
from wpilib.shuffleboard import Shuffleboard
from wpimath.geometry import Rotation2d

class SwerveModule():
    """Class for controlling swerve module on robot."""

    def __init__(self, module_position, steering_motor_id, driving_motor_id, cancoder_id, default_cancoder_value, module_direction):
        """
        Constructor for Swerve Module.

        :param module_position: Location of the module. Possible options: FR, FL, BR, BL
        :type module_position: str
        :param steering_motor_id: ID of the steering motor
        :type steering_motor_id: int
        :param driving_motor_id: ID of the driving motor
        :type driving_motor_id: int
        :param cancoder_id: ID of the CANcoder
        :type cancoder_id: int
        :param default_cancoder_value: Default value of the CANcoder at 0 degrees. Only used when Shuffleboard widget is not accessible.
        :type default_cancoder_value: float
        :param module_direction: Direction the module faces. 1 is forward relative to the front of the robot. -1 is inverted relative to the front of the robot.
        :type module_direction: int, 1 or -1
        """        
        # Hardware Initialization
        self.steering_motor = phoenix6.hardware.TalonFX(steering_motor_id)
        self.driving_motor = phoenix6.hardware.TalonFX(driving_motor_id)
        self.cancoder = phoenix6.hardware.CANcoder(cancoder_id)
        self.module_position = module_position

        # Turning Motor Configs
        self.talonfx_configs = phoenix6.configs.TalonFXConfiguration()
        self.talonfx_configs.closed_loop_general.continuous_wrap = True
        self.talonfx_configs.feedback.sensor_to_mechanism_ratio = 150 / 7

        # PID Configs
        self.talonfx_configs.slot0.k_p = 20
        self.talonfx_configs.slot0.k_i = 0 
        self.talonfx_configs.slot0.k_d = 0

        # Apply the configs to the steering motor
        self.steering_motor.configurator.apply(self.talonfx_configs) 

        # Create PID object
        self.pid = phoenix6.controls.PositionVoltage(0).with_slot(0)

        # Cancoder Config
        self.default_cancoder_value = default_cancoder_value
        self.get_default_cancoder_value()
        
        # Swerve Module Configs
        self.determine_steering_motor_offset()   
        self.module_direction = module_direction
        self.current_angle = None

    def _get_default_cancoder_value(self):
        """
        Get the default CANcoder value from Shuffleboard.
        """
        self.default_cancoder_value = Shuffleboard.getTab("CANcoders").add(f"{self.module_position} Default CANcoder Value", 
                                                                           self.default_cancoder_value).getEntry().getFloat(self.default_cancoder_value)  

    def _determine_steering_motor_offset(self):
        """
        Determine the steering motor offset to allow the swerve module to face forward.
        """
        # Calculate CANcoder offsets for 0 degree position
        cancoder_offset = self.default_cancoder_value - self.cancoder.get_absolute_position().value

        # Set steering motor offset
        self.steering_motor_offset = self.steering_motor.get_position().value - cancoder_offset

    def reset(self):
        """
        Reset the swerve module's main variables and set it to face forward.
        """
        self.get_default_cancoder_value()
        self.determine_steering_motor_offset()
        self.current_angle = Rotation2d.fromDegrees(0)
        self.steering_motor.set_control(self.pid.with_position(self.steering_motor_offset)) 

    def stop(self):
        """
        Stop the driving motor but continue to hold the last position received from the joystick.
        """
        self.driving_motor.set_control(phoenix6.controls.DutyCycleOut(0))

    def move(self, speed, angle):
        """
        Move the Swerve Module to the desired speed and angle.
    
        :param speed: Desired speed of the module. Must be between 0 and 1. Use wpimath.kinematics.SwerveDrive4Kinematics.desaturateWheelSpeeds 
        to reduce desired speed to be between 0 and 1. 
        :type speed: float
        :param angle: Desired angle of the module. Must already be optimized. Use wpimath.kinematics.SwerveModuleState.optimize to optimize the angle.
        :type angle: float
        """
        # Determine speed, position, and module direction
        desired_speed = speed
        desired_angle = ((angle.degrees() * -1) + 360) % 360
        desired_position = self.steering_motor_offset + (desired_angle / 360)
        self.current_angle = angle

        # Set the motors to the desired speed and angle
        self.driving_motor.set_control(phoenix6.controls.DutyCycleOut(desired_speed * self.module_direction))
        self.steering_motor.set_control(self.pid.with_position(desired_position)) 
