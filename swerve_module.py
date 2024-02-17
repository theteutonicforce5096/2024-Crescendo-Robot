import phoenix6
from wpilib.shuffleboard import Shuffleboard
from wpimath.geometry import Rotation2d

class SwerveModule():
    """Class for controlling swerve module on robot."""

    def __init__(self, module_position, steering_motor_id, driving_motor_id, cancoder_id, steering_motor_bus, driving_motor_bus, cancoder_bus, default_cancoder_value, inverted_module):
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
        :param inverted_module: Whether the module is inverted or not.
        :type inverted_module: boolean
        """        
        # Hardware Initialization
        self.steering_motor = phoenix6.hardware.TalonFX(steering_motor_id, steering_motor_bus)
        self.driving_motor = phoenix6.hardware.TalonFX(driving_motor_id, driving_motor_bus)
        self.cancoder = phoenix6.hardware.CANcoder(cancoder_id, cancoder_bus)
        self.module_position = module_position

        # Steering Motor and Driving Motor Config
        self._configure_driving_motor(inverted_module)
        self._configure_steering_motor()

        # Cancoder Config
        self.default_cancoder_value = default_cancoder_value
        self._get_default_cancoder_value()
        
        # Swerve Module Configs
        self._determine_steering_motor_offset()   
        self.current_angle = None

    def _configure_driving_motor(self, inverted_module):
        # Driving Motor Configs
        talonfx_configs = phoenix6.configs.TalonFXConfiguration()
        talonfx_configs.closed_loop_general.continuous_wrap = True
        talonfx_configs.feedback.sensor_to_mechanism_ratio = 6.12
        talonfx_configs.closed_loop_ramps.voltage_closed_loop_ramp_period = 0.2
        if inverted_module:
            talonfx_configs.motor_output.inverted = phoenix6.signals.InvertedValue.CLOCKWISE_POSITIVE

        # PID Configs
        talonfx_configs.slot0.k_s = 0.05
        talonfx_configs.slot0.k_v = 0.12
        talonfx_configs.slot0.k_p = 0.75
        talonfx_configs.slot0.k_i = 0 
        talonfx_configs.slot0.k_d = 0

        # Apply the configs to the driving motor
        self.driving_motor.configurator.apply(talonfx_configs) 

        # Create PID object
        self.driving_pid = phoenix6.controls.VelocityVoltage(velocity = 0, enable_foc = False)

    def _configure_steering_motor(self):
        # Steering Motor Configs
        talonfx_configs = phoenix6.configs.TalonFXConfiguration()
        talonfx_configs.closed_loop_general.continuous_wrap = True
        talonfx_configs.feedback.sensor_to_mechanism_ratio = 150 / 7
        talonfx_configs.closed_loop_ramps.voltage_closed_loop_ramp_period = 0.2

        # PID Configs
        talonfx_configs.slot0.k_p = 10
        talonfx_configs.slot0.k_i = 0 
        talonfx_configs.slot0.k_d = 0

        # Apply the configs to the steering motor
        self.steering_motor.configurator.apply(talonfx_configs) 

        # Create PID object
        self.steering_pid = phoenix6.controls.PositionVoltage(position = 0, enable_foc = False)

    def _get_default_cancoder_value(self):
        """
        Get the default CANcoder value for SwerveModule from Shuffleboard.
        """
        self.default_cancoder_value = Shuffleboard.getTab("CANcoders").add(f"{self.module_position} Default CANcoder Value", self.default_cancoder_value).getEntry().getFloat(self.default_cancoder_value)  

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
        Reset the swerve module's main variables and set it to hold its position.
        """
        self._get_default_cancoder_value()
        self._determine_steering_motor_offset()
        self.current_angle = Rotation2d.fromDegrees(0)
        self.driving_motor.set_control(self.driving_pid.with_velocity(0))
        self.steering_motor.set_control(self.steering_pid.with_position(self.steering_motor_offset)) 

    def stop(self):
        """
        Stop the driving motor but continue to hold the last position received from the joystick.
        """
        self.driving_motor.set_control(self.driving_pid.with_velocity(0))

    def set(self, speed, angle):
        """
        Set the Swerve Module to a desired speed and angle.
    
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
        self.driving_motor.set_control(self.driving_pid.with_velocity(desired_speed * (100 / 6.12)))
        self.steering_motor.set_control(self.steering_pid.with_position(desired_position)) 
