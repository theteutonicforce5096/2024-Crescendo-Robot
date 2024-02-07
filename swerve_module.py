import phoenix6
from wpilib.shuffleboard import Shuffleboard

class SwerveModule():
    """Class for controlling swerve module on robot."""

    def __init__(self, module_position, steering_motor_id, driving_motor_id, cancoder_id, default_cancoder_value):
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
        """

        # Hardware Initialization
        self.steering_motor = phoenix6.hardware.TalonFX(steering_motor_id)
        self.driving_motor = phoenix6.hardware.TalonFX(driving_motor_id)
        self.cancoder = phoenix6.hardware.CANcoder(cancoder_id)

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

        # Cancoder Configs
        self.cancoders = Shuffleboard.getTab("CANcoders")
        self.default_cancoder_value = self.cancoders.add(f"{module_position} Default CANcoder Value", default_cancoder_value).getEntry().getFloat(default_cancoder_value)  

        # Motor Offset and Starting Direction
        self.steering_motor_offset = self.determine_steering_motor_offset()      

    def determine_steering_motor_offset(self):
        """
        Determine the steering motor offset to allow the swerve module to face forward and return the steering motor offset and module direction.
        """
        # Calculate CANcoder offsets for 0 degree position
        cancoder_offset = self.default_cancoder_value - self.cancoder.get_absolute_position().value

        # Set steering motor offset to the opossite of the 
        steering_motor_offset = self.steering_motor.get_position().value - cancoder_offset

        # Return steering motor offset 
        return steering_motor_offset

    def reset(self):
        """
        Set the swerve module to face forward.
        """
        self.steering_motor.set_control(self.pid.with_position(self.steering_motor_offset)) 

    def set_velocity(self, speed, angle, direction = 1):
        """
        Set the velocity of the swerve module.
    
        :param speed: Desired speed of the module. Must be between 0 and 1. Use wpimath.kinematics.SwerveDrive4Kinematics.desaturateWheelSpeeds 
        to reduce desired speed to be between 0 and 1. 
        :type speed: float
        :param angle: Desired angle of the module. Must already be optimized. Use wpimath.kinematics.SwerveModuleState.optimize to optimize the angle.
        :type angle: float
        :param direction: Direction of the motor. 1 is facing forward. -1 is inverted. Use the direction from wpimath.kinematics.SwerveModuleState.optimize.
        :type direction: int. 1 or -1
        """
        # Determine speed, position, and module direction
        desired_speed = speed
        desired_position = self.steering_motor_offset + (angle / 360)
        desired_module_direction = direction

        # Set the motors to the desired speed and angle
        self.driving_motor.set_control(phoenix6.controls.DutyCycleOut(desired_speed * desired_module_direction))
        self.steering_motor.set_control(self.pid.with_position(desired_position)) 
