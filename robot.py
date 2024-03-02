import wpilib
from drivetrain import SwerveDrive
from shooter import Shooter
from arm import Arm
from color_sensor import ColorSensor
import phoenix6

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Initialize components
        self.drivetrain = SwerveDrive()
        self.shooter = Shooter(40, 41, 42, False, False, False, 0.5)
        self.arm = Arm()
        self.color_sensor = ColorSensor()

        # Initialize controllers
        self.drivetrain_controller = wpilib.XboxController(0)
        self.shooter_controller = wpilib.XboxController(1)

        # Initialize timer
        self.timer = wpilib.Timer()
        self.drivetrain_timer = wpilib.Timer()
        self.drop_timer = wpilib.Timer()
        self.prime_shooter_timer = wpilib.Timer()
        self.shoot_timer = wpilib.Timer()

        self.right_motor = phoenix6.hardware.TalonFX(51)
        self.left_motor = phoenix6.hardware.TalonFX(50)

        # Set default robot speeds
        self.forward_speed = 0
        self.strafe_speed = 0
        self.rotation_speed = 0

    def teleopInit(self):
        # Reset timers
        self.timer.restart()
        self.drivetrain_timer.reset()
        self.drop_timer.reset()
        self.prime_shooter_timer.reset()
        self.shoot_timer.reset()

        # Reset robot speeds.
        self.forward_speed = 0
        self.strafe_speed = 0
        self.rotation_speed = 0

        # Reset Drivetrain
        self.drivetrain.reset_drivetrain()
        self.drivetrain.reset_gyro()

        # Reset shooter
        self.shooter.reset()

        # Enable Drivetrain
        self.drivetrain.change_drivetrain_state("Enabled")

        # Enable Shooter
        self.shooter.change_shooter_state("Idle")

    def teleopPeriodic(self):
        # Get speeds from drivetrain controller.
        forward_speed = self.drivetrain_controller.getLeftY()
        strafe_speed = self.drivetrain_controller.getLeftX()
        rotation_speed = self.drivetrain_controller.getRightX()

        # Check if gyro needs to be reset.
        if self.drivetrain_controller.getAButtonPressed():
            self.drivetrain.stop_robot()
            self.drivetrain.reset_gyro()
            self.drivetrain_timer.restart()
            self.drivetrain.change_drivetrain_state("Resetting Gyro")

        if self.drivetrain_controller.getBButtonPressed():
            # Forward
            self.right_motor.set_control(phoenix6.controls.DutyCycleOut(0.25))
            self.left_motor.set_control(phoenix6.controls.DutyCycleOut(-0.25))
        elif self.drivetrain_controller.getXButtonPressed():
            # Backward
            self.right_motor.set_control(phoenix6.controls.DutyCycleOut(-0.25))
            self.left_motor.set_control(phoenix6.controls.DutyCycleOut(0.25))
        elif self.drivetrain_controller.getYButtonPressed():
            self.right_motor.set_control(phoenix6.controls.DutyCycleOut(0))
            self.left_motor.set_control(phoenix6.controls.DutyCycleOut(0))

        # Check if max drivetrain speed needs to be changed.
        if (self.drivetrain_controller.getLeftTriggerAxis() > 0.1) != (self.drivetrain_controller.getRightTriggerAxis() > 0.1):
            self.drivetrain.change_max_drivetrain_speed(0.75)
        elif self.drivetrain_controller.getLeftTriggerAxis() > 0.1 and self.drivetrain_controller.getRightTriggerAxis() > 0.1:
            self.drivetrain.change_max_drivetrain_speed(1.0)
        else:
            self.drivetrain.change_max_drivetrain_speed(0.5)

        # Set deadzone on forward speed.
        if forward_speed > 0.1 or forward_speed < -0.1:
            self.forward_speed = forward_speed
        else:
            self.forward_speed = 0

        # Set deadzone on strafe speed.
        if strafe_speed > 0.1 or strafe_speed < -0.1:
            self.strafe_speed = strafe_speed
        else:
            self.strafe_speed = 0

        # Set deadzone on rotation speed.
        if rotation_speed > 0.1 or rotation_speed < -0.1:
            self.rotation_speed = rotation_speed
        else:
            self.rotation_speed = 0

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
                    self.drivetrain.change_drivetrain_state("Disabled")
                    self.shooter.prime_shooter()
                    # Change Arm position
                    self.prime_shooter_timer.restart()
                    self.shooter.change_shooter_state("Armed")
                elif self.shooter_controller.getBButtonPressed():
                    self.drivetrain.change_drivetrain_state("Disabled")
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
                self.drivetrain.change_drivetrain_state("Enabled")
                self.shooter.reset()
                self.shooter.change_shooter_state("Idle")

        # Move robot if drivetrain is enabled.
        match self.drivetrain.get_drivetrain_state():
            case "Enabled":
                if self.forward_speed != 0 or self.strafe_speed != 0 or self.rotation_speed != 0:
                    self.drivetrain.move_robot(self.forward_speed, self.strafe_speed, self.rotation_speed) 
                else:
                    self.drivetrain.stop_robot()
            case "Resetting Gyro":
                if not self.drivetrain_timer.hasElapsed(0.5):
                    if self.forward_speed != 0 or self.strafe_speed != 0 or self.rotation_speed != 0:
                        self.drivetrain_controller.setRumble(wpilib.XboxController.RumbleType.kBothRumble, 0.75)  
                    else:
                        self.drivetrain_controller.setRumble(wpilib.XboxController.RumbleType.kBothRumble, 0)  
                else:
                    self.drivetrain_controller.setRumble(wpilib.XboxController.RumbleType.kBothRumble, 0)  
                    self.drivetrain_timer.reset()
                    self.drivetrain.change_drivetrain_state("Enabled")
            case "Disabled":
                if self.forward_speed != 0 or self.strafe_speed != 0 or self.rotation_speed != 0:
                    self.drivetrain_controller.setRumble(wpilib.XboxController.RumbleType.kBothRumble, 0.75)  
                else:
                    self.drivetrain_controller.setRumble(wpilib.XboxController.RumbleType.kBothRumble, 0) 

            #self.arm.update_pid_controller() 

    def disabledInit(self):
        # Turn off drivetrain controller rumble if it is stil on.
        self.drivetrain_controller.setRumble(wpilib.XboxController.RumbleType.kBothRumble, 0)  

if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
