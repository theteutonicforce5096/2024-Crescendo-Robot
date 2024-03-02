import phoenix6
from wpilib.shuffleboard import Shuffleboard
from wpilib import DutyCycleEncoder
from wpimath.controller import PIDController
from math import pi, cos

class Arm():
    """Class for controlling arm on robot."""

    def __init__(self, left_motor_id, right_motor_id, left_motor_inverted, right_motor_inverted, encoder_id, encoder_0_position, encoder_lower_bound):
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
        :param encoder_lower_bound: Value of the Encoder when the Arm is at its lowest possible position. Used as a default for Shuffleboard widget.
        :type encoder_lower_bound: float
        """        
        # Hardware initialization
        self.left_motor = phoenix6.hardware.TalonFX(left_motor_id)
        self.right_motor = phoenix6.hardware.TalonFX(right_motor_id)
        self.encoder = DutyCycleEncoder(encoder_id)

        #self.p_widget = Shuffleboard.getTab("Arm").add(f"P", 0.0).withSize(2, 2).getEntry()
        #self.i_widget = Shuffleboard.getTab("Arm").add(f"I", 0.0).withSize(2, 2).getEntry()
        #self.d_widget = Shuffleboard.getTab("Arm").add(f"D", 0.0).withSize(2, 2).getEntry()

        # PID Controller
        self.arm_controller = PIDController(100, 0, 0)
        self.arm_controller.enableContinuousInput(0, 1)
        self.static_gain = 0
        self.gravity_gain = 0.29
        
        # Encoder configs
        self.encoder_0_position = Shuffleboard.getTab("Arm").add(f"0 Position Arm Encoder Value", encoder_0_position).withSize(2, 2).getEntry().getFloat(encoder_0_position) 
        self.encoder_lower_bound = Shuffleboard.getTab("Arm").add(f"Lowest Position Arm Encoder Value", encoder_lower_bound).withSize(2, 2).getEntry().getFloat(encoder_lower_bound)   

        # Arm Configs
        self.arm_state = "Disabled"
        self.current_angle = None
        self.arm_angle_entry = Shuffleboard.getTab("Drivers").add(f"Arm Angle", "None").withSize(2, 2).getEntry()
        self.arm_setpoint_entry = Shuffleboard.getTab("Drivers").add(f"Arm Setpoint", "0").withSize(2, 2).getEntry()
        
        self._configure_arm_motor(self.left_motor, left_motor_inverted)
        self._configure_arm_motor(self.right_motor, right_motor_inverted)

    def _configure_arm_motor(self, motor, inverted_module):
        # Arm Motor Configs
        talonfx_configs = phoenix6.configs.TalonFXConfiguration()
        
        if inverted_module:
            talonfx_configs.motor_output.inverted = phoenix6.signals.InvertedValue.CLOCKWISE_POSITIVE

        # Apply the configs to the driving motor
        motor.configurator.apply(talonfx_configs) 

    def _get_encoder_value(self):
        return (self.encoder.getAbsolutePosition() * -1) + 1

    def reset(self):
        """
        Reset the Arm. Set it to 0 degrees. 
        """
        #self.arm_controller.setPID(self.p_widget.getFloat(0.0), self.i_widget.getFloat(0.0), self.d_widget.getFloat(0.0))
        self.set(0)
        self.arm_setpoint_entry.setString("0") 

    def set(self, angle):
        """
        Sets the arm at a certain angle.
        """
        self.arm_controller.setSetpoint(self.encoder_0_position + (angle / 360))
    
    def get_setpoint(self):
        return self.arm_setpoint_entry.getString("0")
        
    def update_pid_controller(self):
        """
        Update output of PID controller.
        """
        self.set(float(self.get_setpoint()))

        encoder_position = self._get_encoder_value()
        print(encoder_position)
        motor_speed = self.arm_controller.calculate(encoder_position)

        angle = encoder_position - self.encoder_0_position
        self.arm_angle_entry.setString(f"{angle * 360}") 

        angle_radians = 2.0 * pi * angle
        feedforward = (self.gravity_gain * cos(angle_radians)) + self.static_gain

        desired_voltage = motor_speed + feedforward

        if encoder_position <= self.encoder_lower_bound and desired_voltage < 0:
            desired_voltage = 0

        self.left_motor.set_control(phoenix6.controls.VoltageOut(desired_voltage))
        self.right_motor.set_control(phoenix6.controls.VoltageOut(desired_voltage))