import phoenix6
from wpilib.shuffleboard import Shuffleboard
from wpilib import DutyCycleEncoder

class Arm():
    """Class for controlling arm on robot."""

    def __init__(self, right_motor_id, left_motor_id, right_motor_bus, left_motor_bus):
        """
        Constructor for Arm.

        :param right_arm_motor_id: ID of right motor on Arm
        :type right_arm_motor_id: int
        :param left_arm_motor_id: ID of left motor on Arm
        :type left_arm_motor_id: int
        """        
        self.right_motor = phoenix6.hardware.TalonFX(right_motor_id, right_motor_bus)
        self.left_motor = phoenix6.hardware.TalonFX(left_motor_id, left_motor_bus).
        self.encoder = DutyCycleEncoder(2)

    def _configure_arm_motor(self, motor, inverted_module):
        # Arm Motor Configs
        talonfx_configs = phoenix6.configs.TalonFXConfiguration()
        talonfx_configs.closed_loop_general.continuous_wrap = True
        talonfx_configs.feedback.sensor_to_mechanism_ratio = 300 / 1
        
        if inverted_module:
            talonfx_configs.motor_output.inverted = phoenix6.signals.InvertedValue.CLOCKWISE_POSITIVE

        # PID Configs
        talonfx_configs.slot0.k_g = 0.25
        talonfx_configs.slot0.gravity_type = phoenix6.signals.spn_enums.GravityTypeValue.ARM_COSINE
        talonfx_configs.slot0.k_p = 1
        talonfx_configs.slot0.k_i = 0 
        talonfx_configs.slot0.k_d = 0

        # Apply the configs to the driving motor
        motor.configurator.apply(talonfx_configs) 

        # Create PID object
        self.driving_pid = phoenix6.controls.PositionVoltage(velocity = 0, enable_foc = False)       