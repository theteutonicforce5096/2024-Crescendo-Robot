import phoenix5
from wpilib.shuffleboard import Shuffleboard
from wpilib import XboxController, Timer
from color_sensor import ColorSensor
from arm import Arm

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
        self.color_sensor = ColorSensor()
        self.arm = Arm()
        
        # Invert motors
        if intake_motor_inverted:
            self._invert_motor(self.intake_motor)

        if flywheel_left_inverted:
            self._invert_motor(self.flywheel_left_motor)

        if flywheel_right_inverted:
            self._invert_motor(self.flywheel_right_motor)
        
        # Initialize shooter controller
        self.shooter_controller = XboxController(1)

        # Intake motor speed
        self.intake_motor_speed = intake_motor_speed

        # Initialize timers
        self.drop_timer = Timer()
        self.prime_shooter_timer = Timer()
        self.shoot_timer = Timer()

        # Set Shooter State
        self.shooter_state = "Idle"
        self.drivers_tab_state = Shuffleboard.getTab("Drivers").add(f"Shooter State", self.shooter_state).withSize(2, 2).getEntry()

    def _invert_motor(self, motor):
        """
        Invert motor.

        :param motor: Motor that needs to be inverted
        :type motor: VictorSPX
        """
        motor.setInverted(True)

    def reset_timers(self):
        """
        Reset shooter timers.
        """
        self.drop_timer.reset()
        self.prime_shooter_timer.reset()
        self.shoot_timer.reset()

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

    def _start_intake_motor(self):
        """
        Start the intake motors.
        """
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, self.intake_motor_speed)

    def _reverse_intake_motor(self):
        """
        Reverse the intake motors.
        """
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, self.intake_motor_speed * -1)

    def _stop_intake_motor(self):
        """
        Stop the intake motors.
        """
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, 0)

    def _prime_shooter(self):
        """
        Turn on the flywheel motors.
        """
        self.flywheel_left_motor.set(phoenix5.ControlMode.PercentOutput, 0.5)
        self.flywheel_right_motor.set(phoenix5.ControlMode.PercentOutput, 0.5)

    def update_shooter(self):
        """
        Update the shooter.
        """ 
        if self.shooter_controller.getYButtonPressed():
            self.change_shooter_state("Reset")
        elif self.shooter_controller.getRightBumperPressed():
            self.change_shooter_state("Force Fire")
        elif self.shooter_controller.getLeftBumperPressed():
            self.change_shooter_state("Drop Everything")

        match self.get_shooter_state():
            case "Idle":
                if self.shooter_controller.getAButtonPressed():
                    self._start_intake_motor()
                    self.change_shooter_state("Collecting")
            case "Collecting":
                if self.color_sensor.detects_ring():
                    self._stop_intake_motor()
                    self.change_shooter_state("Loaded")
            case "Loaded":
                if self.shooter_controller.getXButtonPressed():
                    self._prime_shooter()
                    # Change Arm position
                    self.prime_shooter_timer.restart()
                    self.change_shooter_state("Armed")
                elif self.shooter_controller.getBButtonPressed():
                    self._prime_shooter()
                    # Change Arm position
                    self.prime_shooter_timer.restart()
                    self.change_shooter_state("Armed")
            case "Armed":
                if self.prime_shooter_timer.hasElapsed(2.5):
                    self.prime_shooter_timer.reset()
                    self._start_intake_motor()
                    self.shoot_timer.restart()
                    self.change_shooter_state("Fire")
            case "Fire":
                if self.shoot_timer.hasElapsed(0.5):
                    self.shoot_timer.reset()
                    self.change_shooter_state("Reset")
            case "Force Fire":
                self._prime_shooter()
                self.prime_shooter_timer.restart()
                self.change_shooter_state("Armed")
            case "Drop Everything":
                # Move Arm
                self._reverse_intake_motor()
                self.drop_timer.restart()
                self.change_shooter_state("Stop Dropping Everything")
            case "Stop Dropping Everything":
                # Reset
                if self.drop_timer.hasElapsed(1):
                    self.change_shooter_state("Reset")
            case "Reset":
                self.reset()
                self.change_shooter_state("Idle")

        self.arm.update_position()
