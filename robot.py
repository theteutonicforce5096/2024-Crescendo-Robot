import wpilib
from drivetrain import SwerveDrive
from shooter import Shooter

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Initialize components
        self.drivetrain = SwerveDrive()
        self.shooter = Shooter(9, 8, 6, False, False, False)

        # Initialize timer
        self.timer = wpilib.Timer()

    def teleopInit(self):
        # Reset timers
        self.timer.restart()
        self.drivetrain.reset_timer()
        self.shooter.reset_timers()

        # Reset robot speeds.
        self.drivetrain.reset_robot_speeds()

        # Reset Drivetrain
        self.drivetrain.reset_drivetrain()
        self.drivetrain.reset_gyro()

        # Reset shooter
        self.shooter.reset()

        # Enable Drivetrain
        self.drivetrain.change_drivetrain_state("Enabled")

        # Enable shooter
        self.shooter.change_shooter_state("Idle")

    def teleopPeriodic(self):
        self.drivetrain.update_robot_position()
        self.shooter.update_shooter()

    def disabledInit(self):
        # Turn off drivetrain controller rumble if it is stil on.
        self.drivetrain._set_controller_rumble(0)

if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
