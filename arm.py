import phoenix6
from wpilib.shuffleboard import Shuffleboard
from wpilib import DutyCycleEncoder
from wpimath.controller import PIDController
from math import pi, cos

class Arm():
    """Class for controlling arm on robot."""

    def __init__(self, left_motor_id, right_motor_id, left_motor_inverted, right_motor_inverted, encoder_id, encoder_0_position):
        """
        Constructor for Arm.

        :param right_arm_motor_id: ID of right motor on Arm
        :type right_arm_motor_id: int
        :param left_arm_motor_id: ID of left motor on Arm
        :type left_arm_motor_id: int
        :param left_motor_inverted: Whether the left motor is inverted or not
        :type left_motor_inverted: boolean
        :param right_motor_inverted: Whether the left motor is inverted or not
        :type right_motor_inverted: boolean
        :param encoder_id: ID of encoder on Arm
        :type encoder_id: int
        :param encoder_0_position: Value of the Encoder when the Arm is at 0 degrees (parallel to the ground). Used as a default for Shuffleboard widget.
        :type encoder_0_position: float
        """        
        # Hardware initialization
        self.left_motor = phoenix6.hardware.TalonFX(left_motor_id)
        self.right_motor = phoenix6.hardware.TalonFX(right_motor_id)
        self.encoder = DutyCycleEncoder(encoder_id)

        # PID Controller
        self.arm_controller = PIDController(1, 0 ,0)
        self.arm_controller.enableContinuousInput(0.0, 1.0)
        self.static_gain = 0.05
        self.gravity_gain = 0.25

        # Encoder configs
        self.encoder_0_position = Shuffleboard.getTab("Arm").add(f"0 Position Arm Encoder Value", encoder_0_position).withSize(2, 2).getEntry().getFloat(encoder_0_position)  

        # Arm Configs
        self.arm_state = "Disabled"
        self.current_angle = None
        self.arm_angle_entry = Shuffleboard.getTab("Drivers").add(f"Arm Position", "None").withSize(2, 2).getEntry()
        
        self._configure_arm_motor(self.left_motor, left_motor_inverted)
        self._configure_arm_motor(self.right_motor, right_motor_inverted)

    def _configure_arm_motor(self, motor, inverted_module):
        # Arm Motor Configs
        talonfx_configs = phoenix6.configs.TalonFXConfiguration()
        
        if inverted_module:
            talonfx_configs.motor_output.inverted = phoenix6.signals.InvertedValue.CLOCKWISE_POSITIVE

        # Apply the configs to the driving motor
        motor.configurator.apply(talonfx_configs) 

    def reset(self):
        """
        Reset the Arm. Set it to 45 degrees. 
        """
        self.set(45)

    def set(self, angle):
        """
        Sets the arm at a certain angle.
        """
        self.arm_controller.setSetpoint(self.encoder_0_position + (angle / 360))

    def update_pid_controller(self):
        """
        Update output of PID controller.
        """
        encoder_position = self.encoder.getAbsolutePosition()
        motor_speed = self.arm_controller.calculate(encoder_position)

        angle = encoder_position - self.encoder_0_position
        self.arm_angle_entry.setString(f"{angle * 360}") 

        angle_radians = 2.0 * pi * angle
        feedforward = (self.gravity_gain * cos(angle_radians)) + self.static_gain

        self.left_motor.set_control(phoenix6.controls.VoltageOut(enable_foc = False), motor_speed + feedforward)
        self.right_motor.set_control(phoenix6.controls.VoltageOut(enable_foc = False), motor_speed + feedforward)