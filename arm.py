import phoenix6
from wpilib.shuffleboard import Shuffleboard
from wpilib import DutyCycleEncoder
from wpimath.controller import PIDController
from math import pi, cos

class Arm():
    """Class for controlling arm on robot."""

    def __init__(self, right_motor_id, left_motor_id, right_motor_bus, left_motor_bus, encoder_id, encoder_0_position):
        """
        Constructor for Arm.

        :param right_arm_motor_id: ID of right motor on Arm
        :type right_arm_motor_id: int
        :param left_arm_motor_id: ID of left motor on Arm
        :type left_arm_motor_id: int
        """        
        self.right_motor = phoenix6.hardware.TalonFX(right_motor_id, right_motor_bus)
        self.left_motor = phoenix6.hardware.TalonFX(left_motor_id, left_motor_bus)
        self.encoder = DutyCycleEncoder(encoder_id)
        self.encoder_0_position = encoder_0_position
        self.arm_controller = PIDController(1, 0 ,0)
        self.arm_controller.enableContinuousInput(0.0, 1.0)
        self.arm_state = "Disabled"

        self._configure_arm_motor(self.right_motor, False)
        self._configure_arm_motor(self.left_motor, True)

    def _configure_arm_motor(self, motor, inverted_module):
        # Arm Motor Configs
        talonfx_configs = phoenix6.configs.TalonFXConfiguration()
        talonfx_configs.closed_loop_general.continuous_wrap = True
        talonfx_configs.feedback.sensor_to_mechanism_ratio = 300 / 1
        
        if inverted_module:
            talonfx_configs.motor_output.inverted = phoenix6.signals.InvertedValue.CLOCKWISE_POSITIVE

        # Apply the configs to the driving motor
        motor.configurator.apply(talonfx_configs) 

    def reset(self):
        self.set(0)

    def set(self, angle):
        """
        Sets the arm at a certain angle.
        """
        self.arm_controller.setSetpoint((angle / 360) + self.encoder_0_position)

    def update_position(self):
        """
        Update output of PID controller.
        """
        encoder_position = self.encoder.getAbsolutePosition()
        motor_speed = self.arm_controller.calculate(encoder_position)

        elevation_rad = 2.0 * pi * (encoder_position - self.encoder_0_position)
        gravity_feedforward = 0.25 * cos(elevation_rad)
        motor_speed = min(motor_speed, 0.5)
        motor_speed = max(motor_speed, -0.5)
        motor_speed += gravity_feedforward

        self.left_motor.set_control(phoenix6.ControlMode.PercentOutput, motor_speed)
        self.right_motor.set_control(phoenix6.ControlMode.PercentOutput, motor_speed)

    