import wpilib
from drivetrain import SwerveDrive
from shooter import Shooter
from color_sensor import ColorSensor

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Initialize components
        self.drivetrain = SwerveDrive()
        self.shooter = Shooter(9, 8, 6, 10, 31)
        self.color_sensor = ColorSensor()

        self.shooter_controller = wpilib.XboxController(1)

        # Initialize timer
        self.timer = wpilib.Timer()
        self.drop_timer = wpilib.Timer()
        self.prime_shooter_timer = wpilib.Timer()
        self.shoot_timer = wpilib.Timer()

    def teleopInit(self):
        # Reset timers
        self.timer.restart()
        self.drivetrain.reset_timer()
        self.drop_timer.reset()
        self.prime_shooter_timer.reset()
        self.shoot_timer.reset()

        # Reset robot speeds.
        self.drivetrain.reset_robot_speeds()

        # Reset Drivetrain
        self.drivetrain.reset_drivetrain()
        self.drivetrain.reset_gyro()

        # Enable Drivetrain
        self.drivetrain.change_drivetrain_state("Enabled")

        # Enable shooter
        self.shooter.change_shooter_state("Idle")

    def teleopPeriodic(self):
        self.drivetrain.update_robot_position()

        if self.shooter_controller.getYButtonPressed():
            self.shooter_state = "Reset"
        elif self.shooter_controller.getRightBumperPressed():
            self.shooter_state = "Force Arm"
        elif self.shooter_controller.getLeftBumperPressed():
            self.shooter_state = "Drop Everything"

        match self.shooter.get_shooter_state():
            case "Idle":
                if self.joystick.getRawButtonPressed(2):
                    self.shooter.pick_up_note()
                    self.shooter.change_shooter_state("Collecting")
            case "Collecting":
                if self.color_sensor.detects_ring():
                    self.shooter.stop_picking_up_note()
                    self.shooter_state = "Loaded"
            case "Loaded":
                if self.joystick.getRawButtonPressed(1):
                    self.shooter.prime_shooter()
                    self.prime_shooter_timer.restart()
                    self.shooter_state = "Armed"
            case "Armed":
                if self.prime_shooter_timer.hasElapsed(2.5):
                    if self.joystick.getRawButtonPressed(1):
                        self.prime_shooter_timer.reset()
                        self.shooter.fire_out_note()
                        self.shoot_timer.restart()
                        self.shooter_state = "Fire"
            case "Fire":
                if self.shoot_timer.hasElapsed(0.5):
                    self.shoot_timer.reset()
                    self.shooter_state = "Reset"
            case "Force Arm":
                self.shooter.prime_shooter()
                self.prime_shooter_timer.restart()
                self.shooter_state = "Force Fire"
            case "Force Fire":
                if self.prime_shooter_timer.hasElapsed(2.5):
                    self.prime_shooter_timer.reset()
                    self.shooter.fire_out_note()
                    self.shoot_timer.restart()
                    self.shooter_state = "Stop Force Fire"
            case "Stop Force Fire":
                if self.shoot_timer.hasElapsed(0.5):
                    self.shoot_timer.reset()
                    self.shooter_state = "Reset"
            case "Drop Everything":
                self.shooter.drop_everything()
                self.drop_timer.restart()
                self.shooter_state = "Stop Dropping Everything"
            case "Stop Dropping Everything":
                if self.drop_timer.hasElapsed(1):
                    self.shooter_state = "Reset"
            case "Reset":
                self.shooter.reset()
                self.shooter_state = "Idle"

    def disabledInit(self):
        # Turn off drivetrain controller rumble if it is stil on.
        self.drivetrain._set_controller_rumble(0)

if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
