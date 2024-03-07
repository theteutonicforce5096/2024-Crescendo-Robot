import phoenix5
from wpilib.shuffleboard import Shuffleboard

class Shooter():
    """Class for controlling shooter on robot."""
    def __init__(self, intake_motor_id, flywheel_left_motor_id, flywheel_right_motor_id, intake_motor_inverted, flywheel_left_inverted, flywheel_right_inverted, intake_motor_speed):
        """
        Constructor for Swerve Module.

        :param intake_motor_id: ID of the intake motor
        :type intake_motor_id: int
        :param flywheel_left_motor_id: ID of the flywheel left motor
        :type flywheel_left_motor_id: int
        :param flywheel_right_motor_id: ID of the flywheel right motor
        :type flywheel_right_motor_id: int
        :param intake_motor_inverted: Whether the motor is inverted or not.
        :type intake_motor_inverted: boolean
        :param flywheel_left_inverted: Whether the motor is inverted or not.
        :type flywheel_left_inverted: boolean
        :param flywheel_right_inverted: Whether the motor is inverted or not.
        :type flywheel_right_inverted: boolean
        :param intake_motor_speed: Speed of the intake motor.
        :type intake_motor_speed: float
        """        
        # Hardware initialization
        self.intake_motor = phoenix5.VictorSPX(intake_motor_id)
        self.flywheel_left_motor = phoenix5.VictorSPX(flywheel_left_motor_id)
        self.flywheel_right_motor = phoenix5.VictorSPX(flywheel_right_motor_id)

        # Configure motors
        self._configure_motor(self.intake_motor)
        self._configure_motor(self.flywheel_left_motor)
        self._configure_motor(self.flywheel_right_motor)
        
        # Invert motors
        if intake_motor_inverted:
            self._invert_motor(self.intake_motor)

        if flywheel_left_inverted:
            self._invert_motor(self.flywheel_left_motor)

        if flywheel_right_inverted:
            self._invert_motor(self.flywheel_right_motor)

        # Intake motor speed
        self.intake_motor_speed = intake_motor_speed
  
        # Set Shooter State
        self.shooter_state = "Idle"
        self.drivers_tab_state = Shuffleboard.getTab("Drivers").add(f"Shooter State", self.shooter_state).withSize(2, 2).getEntry()
        self.shooter_speed_widget = Shuffleboard.getTab("Drivers").add(f"Shooter Speed", 1.0).withSize(2, 2).getEntry()

    def _invert_motor(self, motor):
        """
        Invert motor.

        :param motor: Motor that will to be inverted
        :type motor: VictorSPX
        """
        motor.setInverted(True)

    def _configure_motor(self, motor):
        """
        Configures a flywheel motor.

        :param motor: Motor that will be configured
        :type motor: VictorSPX
        """
        motor.configVoltageCompSaturation(12.0)
        motor.enableVoltageCompensation(True)

    def reset(self):
        """
        Reset motors.
        """
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, 0)
        self.flywheel_left_motor.set(phoenix5.ControlMode.PercentOutput, 0)
        self.flywheel_right_motor.set(phoenix5.ControlMode.PercentOutput, 0)

    def get_shooter_state(self):
        """
        Get the shooter's state.
        """
        return self.shooter_state
    
    def change_shooter_state(self, state):
        """
        Change the shooter's state.

        :param state: State of the shooter
        :type state: str
        """
        self.shooter_state = state
        self.drivers_tab_state.setString(self.shooter_state)

    def start_intake_motor(self):
        """
        Start the intake motors.
        """
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, self.intake_motor_speed)

    def reverse_intake_motor(self):
        """
        Reverse the intake motors.
        """
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, self.intake_motor_speed * -1)

    def stop_intake_motor(self):
        """
        Stop the intake motors.
        """
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, 0)

    def prime_shooter(self):
        """
        Turn on the flywheel motors.
        """
        self.flywheel_left_motor.set(phoenix5.ControlMode.PercentOutput, self.shooter_speed_widget.getFloat(0))
        self.flywheel_right_motor.set(phoenix5.ControlMode.PercentOutput, self.shooter_speed_widget.getFloat(0))