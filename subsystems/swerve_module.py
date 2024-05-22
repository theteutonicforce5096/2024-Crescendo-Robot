import phoenix6
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition
from math import pi

class SwerveModule():
    """Class for controlling swerve module on robot."""

    def __init__(self, steering_motor_id, driving_motor_id, cancoder_id, steering_motor_bus, driving_motor_bus, cancoder_bus, cancoder_offset, inverted_module):
        """
        Constructor for Swerve Module.

        :param steering_motor_id: ID of the steering motor
        :type steering_motor_id: int
        :param driving_motor_id: ID of the driving motor
        :type driving_motor_id: int
        :param cancoder_id: ID of the CANcoder
        :type cancoder_id: int
        :param steering_motor_bus: CANbus the steering motor is on
        :type steering_motor_bus: str
        :param driving_motor_bus: CANbus the driving motor is on
        :type driving_motor_bus: str
        :param cancoder_offset: CANcoder absolute encoder offset
        :type cancoder_offset: float
        :param inverted_module: Whether the module is inverted or not.
        :type inverted_module: boolean
        """        

        # Hardware Initialization 
        self.steering_motor = phoenix6.hardware.TalonFX(steering_motor_id, steering_motor_bus)
        self.driving_motor = phoenix6.hardware.TalonFX(driving_motor_id, driving_motor_bus)
        self.cancoder = phoenix6.hardware.CANcoder(cancoder_id, cancoder_bus)

        # Hardware Configuration
        self._configure_driving_motor(inverted_module)
        self._configure_steering_motor()
        self._configure_cancoder(cancoder_offset)

        # Swerve Module Variables
        self.steering_offset = cancoder_offset
        self.position = SwerveModulePosition()
        self.update_position()

    def _configure_cancoder(self, cancoder_offset):
        """
        Configure the CANcoder.

        :param cancoder_offset: CANcoder absolute encoder offset
        :type cancoder_offset: float
        """
        cancoder_configs = phoenix6.configs.CANcoderConfiguration()

        # CANcoder range
        cancoder_configs.magnet_sensor.absolute_sensor_range = phoenix6.signals.spn_enums.AbsoluteSensorRangeValue.UNSIGNED_0_TO1

        # CANcoder offset
        cancoder_configs.magnet_sensor.magnet_offset = cancoder_offset

        # Apply the configs to the CANcoder
        self.cancoder.configurator.apply(cancoder_configs) 

    def _configure_driving_motor(self, inverted_module):
        """
        Configure the driving motor.
    
        :param inverted_module: Whether the module is inverted or not.
        :type inverted_module: bool
        """
        driving_motor_configs = phoenix6.configs.TalonFXConfiguration()
        driving_motor_configs.feedback.sensor_to_mechanism_ratio = 6.12
        if inverted_module:
            driving_motor_configs.motor_output.inverted = phoenix6.signals.InvertedValue.CLOCKWISE_POSITIVE
        
        # Supply limit
        driving_motor_configs.current_limits.stator_current_limit_enable = True
        driving_motor_configs.current_limits.stator_current_limit = 55

        # PID Configs
        driving_motor_configs.slot0.k_s = 0.18
        driving_motor_configs.slot0.k_v = 0.13757366
        driving_motor_configs.slot0.k_a = 0.01267852
        driving_motor_configs.slot0.k_p = 0.11
        driving_motor_configs.slot0.k_i = 0 
        driving_motor_configs.slot0.k_d = 0 

        # Motion Magic
        driving_motor_configs.motion_magic.motion_magic_acceleration = 100
        driving_motor_configs.motion_magic.motion_magic_jerk = 1500

        # Apply the configs to the driving motor
        self.driving_motor.configurator.apply(driving_motor_configs) 

        # Create PID object
        self.driving_pid = phoenix6.controls.MotionMagicVelocityVoltage(velocity = 0, enable_foc = False)

    def _configure_steering_motor(self):
        """
        Configure the steering motor.
        """
        # Steering Motor Configs
        steering_motor_configs = phoenix6.configs.TalonFXConfiguration()
        steering_motor_configs.closed_loop_general.continuous_wrap = True
        steering_motor_configs.feedback.sensor_to_mechanism_ratio = 150 / 7
        
        # Supply limit
        steering_motor_configs.current_limits.stator_current_limit_enable = True
        steering_motor_configs.current_limits.stator_current_limit = 25

        # PID Configs
        steering_motor_configs.slot0.k_p = 100
        steering_motor_configs.slot0.k_i = 0
        steering_motor_configs.slot0.k_d = 0

        # Apply the configs to the steering motor
        self.steering_motor.configurator.apply(steering_motor_configs) 

        # Create PID object
        self.steering_pid = phoenix6.controls.PositionVoltage(position = 0, enable_foc = False)

    def get_angle(self):
        self.update_position()
        return self.position.angle

    def get_position(self):
        self.update_position()
        return self.position

    def update_position(self):
        angle = (self.cancoder.get_absolute_position().value * 360) % 360
        if angle > 180:
            angle -= 360
        elif angle <= -180:
            angle += 360

        self.position.angle = Rotation2d.fromDegrees(angle)
        self.position.distance = self.driving_motor.get_position().value * 0.1016 * pi

    def reset(self):
        """
        Reset the swerve module's main variables and set it to hold its position.
        """
        self.steering_motor.set_control(self.steering_pid.with_position(self.steering_offset)) 
        self.driving_motor.set_control(self.driving_pid.with_velocity(0))

    def stop(self):
        """
        Stop the driving motor but continue to hold the last position received from the joystick.
        """
        self.driving_motor.set_control(self.driving_pid.with_velocity(0))

    def set(self, speed, angle):
        """
        Set the Swerve Module to a desired speed and angle.
    
        :param speed: Desired speed of the module in meters per second.
        :type speed: float
        :param angle: Desired angle of the module. Must already be optimized. Use wpimath.kinematics.SwerveModuleState.optimize to optimize the angle.
        :type angle: float
        """
        # Determine speed, position, and module direction
        desired_speed = speed
        desired_position = self.steering_offset + (((-angle.degrees() + 360) % 360) / 360)

        # Set the motors to the desired speed and angle
        self.steering_motor.set_control(self.steering_pid.with_position(desired_position)) 
        self.driving_motor.set_control(self.driving_pid.with_velocity((desired_speed / 5.21208) * 100))