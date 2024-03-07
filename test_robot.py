import wpilib
from subsystems.arm import Arm
from subsystems.shooter import Shooter
from subsystems.color_sensor import ColorSensor

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Initialize components
        self.arm = Arm(50, 51, True, False, 0, 0.1741)
        self.shooter = Shooter(40, 41, 42, False, False, False, 0.7)
        self.color_sensor = ColorSensor()

        # Initialize controllers
        self.controller = wpilib.XboxController(0)
        self.shooter_controller = wpilib.XboxController(1)

        # Initialize timer
        self.timer = wpilib.Timer()
        self.drop_timer = wpilib.Timer()
        self.prime_shooter_timer = wpilib.Timer()
        self.shoot_timer = wpilib.Timer()

    def teleopInit(self):
        # Reset timers
        self.timer.restart()
        self.drop_timer.reset()
        self.prime_shooter_timer.reset()
        self.shoot_timer.reset()

        self.shooter.reset()

        # Enable Shooter
        self.shooter.change_shooter_state("Idle")

        # Reset Arm
        self.arm.reset()

    def teleopPeriodic(self):
        if self.controller.getAButtonPressed():
            self.arm.set(45)
        elif self.controller.getBButtonPressed():
            self.arm.set(60)
        elif self.controller.getXButtonPressed():
            self.arm.set(70)
        elif self.controller.getYButtonPressed():
            self.arm.set(85)
        elif self.controller.getRightBumperPressed():
            self.arm.set(90)
        elif self.controller.getLeftBumperPressed():
            self.arm.set(95)

        if self.shooter_controller.getYButtonPressed():
            self.shooter.change_shooter_state("Reset")
        elif self.shooter_controller.getRightBumperPressed():
            self.shooter.change_shooter_state("Force Fire")
        elif self.shooter_controller.getLeftBumperPressed():
            self.shooter.change_shooter_state("Drop Everything")

        match self.shooter.get_shooter_state():
            case "Idle":
                if self.shooter_controller.getAButtonPressed():
                    self.shooter.start_intake_motor()
                    self.shooter.change_shooter_state("Collecting")
            case "Collecting":
                if self.color_sensor.detects_ring():
                    self.shooter.stop_intake_motor()
                    self.shooter.change_shooter_state("Loaded")
            case "Loaded":
                if self.shooter_controller.getXButtonPressed():
                    self.shooter.prime_shooter()
                    # Change Arm position
                    self.prime_shooter_timer.restart()
                    self.shooter.change_shooter_state("Armed")
                elif self.shooter_controller.getBButtonPressed():
                    self.shooter.prime_shooter()
                    # Change Arm position
                    self.prime_shooter_timer.restart()
                    self.shooter.change_shooter_state("Armed")
            case "Armed":
                if self.prime_shooter_timer.hasElapsed(2.5):
                    self.prime_shooter_timer.reset()
                    self.shooter.start_intake_motor()
                    self.shoot_timer.restart()
                    self.shooter.change_shooter_state("Fire")
            case "Fire":
                if self.shoot_timer.hasElapsed(0.5):
                    self.shoot_timer.reset()
                    self.shooter.change_shooter_state("Reset")
            case "Force Fire":
                self.shooter.prime_shooter()
                self.prime_shooter_timer.restart()
                self.shooter.change_shooter_state("Armed")
            case "Drop Everything":
                # Move Arm
                self.shooter.reverse_intake_motor()
                self.drop_timer.restart()
                self.shooter.change_shooter_state("Stop Dropping Everything")
            case "Stop Dropping Everything":
                # Reset
                if self.drop_timer.hasElapsed(1):
                    self.shooter.change_shooter_state("Reset")
            case "Reset":
                self.shooter.reset()
                self.shooter.change_shooter_state("Idle")

        self.arm.update_pid_controller() 

if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
