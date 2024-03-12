import phoenix5
from wpilib.shuffleboard import Shuffleboard

class Shooter():
    """Class for controlling shooter on robot."""
    def __init__(self, intake_motor_id, flywheel_left_motor_id, flywheel_right_motor_id, intake_motor_inverted, flywheel_left_inverted, flywheel_right_inverted):
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
  
        # Set Shooter State
        self.shooter_state = "Idle"
        self.next_shooter_state = "None"
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
        motor.enableVoltageCompensation(True)
        # TODO: The context help for enableVoltageCompensation() says that the voltage compensation saturation value must be set FIRST.
        motor.configVoltageCompSaturation(12.0)

    def reset(self):
        """
        Reset motors.
        """
        self.set_intake_motor(0)
        self.set_flywheel_motors(0)

        self.change_shooter_state("Idle")
        self.change_next_shooter_state("None")

    def get_shooter_state(self):
        """
        Get the shooter's state.
        """
        return self.shooter_state
    
    def get_next_shooter_state(self):
        """
        Get the next shooter state.
        """
        return self.next_shooter_state
    
    def change_shooter_state(self, state):
        """
        Change the shooter's state.

        :param state: State of the shooter
        :type state: str
        """
        self.shooter_state = state
        self.drivers_tab_state.setString(self.shooter_state)

    def change_next_shooter_state(self, state):
        """
        Change the next shooter state.

        :param state: Next state of the shooter
        :type state: str
        """
        self.next_shooter_state = state

    def set_intake_motor(self, speed):
        """
        Set the intake motors to a specific speed.

        :param speed: Desired speed of the intake motors.
        :type speed: float
        """
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, speed)

    def set_flywheel_motors(self, speed):
        """
        Set the flywheel motors to a specific speed.

        :param speed: Desired speed of the flywheel motors.
        :type speed: float
        """
        self.flywheel_left_motor.set(phoenix5.ControlMode.PercentOutput, speed)
        self.flywheel_right_motor.set(phoenix5.ControlMode.PercentOutput, speed)

    def start_flywheel_motors(self):
        """
        Turn on the flywheel motors.
        """
        self.flywheel_left_motor.set(phoenix5.ControlMode.PercentOutput, self.shooter_speed_widget.getFloat(1.0))
        self.flywheel_right_motor.set(phoenix5.ControlMode.PercentOutput, self.shooter_speed_widget.getFloat(1.0))

    def predict_speaker_shooting_state(self, distance):
        """
        Predict the arm angle and flywheel speed for shooting at the speaker.

        :param: distance: Distance, in meters, away from the Speaker.
        :type distance: float
        """
        arm_angle = distance * 5 + 1
        flywheel_speed = distance * 2 + 3
        return arm_angle, flywheel_speed