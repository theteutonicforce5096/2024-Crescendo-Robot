import wpilib
from drivetrain import SwerveDrive
from shooter import Shooter
from color_sensor import ColorSensor

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.drivetrain = SwerveDrive()
        self.shooter = Shooter(9, 8, 6, 10, 31)
        self.color_sensor = ColorSensor()
        self.joystick = wpilib.Joystick(0)
        self.controller = wpilib.XboxController(1)

        self.timer = wpilib.Timer()
        self.drop_timer = wpilib.Timer()
        self.prime_shooter_timer = wpilib.Timer()
        self.shoot_timer = wpilib.Timer()

        # Custom Variables
        self.shooter_state = "Idle"
        self.forward_speed = 0
        self.strafe_speed = 0
        self.rotation_speed = 0

    def autonomousInit(self):
        self.timer.restart()
        self.drop_timer.reset()
        self.prime_shooter_timer.reset()
        self.shoot_timer.reset()        
        
        self.drivetrain.reset_drivetrain()
        self.drivetrain.reset_gyro()

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.timer.restart()
        self.drop_timer.reset()
        self.prime_shooter_timer.reset()
        self.shoot_timer.reset()

        # Reset Custom Variables
        self.forward_speed = 0
        self.strafe_speed = 0
        self.rotation_speed = 0
        self.shooter_state = "Idle"

        self.drivetrain.reset_drivetrain()
        self.drivetrain.reset_gyro()
        self.shooter.reset()

    def teleopPeriodic(self):
        forward_speed = self.controller.getLeftY()
        strafe_speed = self.controller.getLeftX()
        rotation_speed = self.controller.getRightX()

        if self.controller.getAButtonPressed():
            self.drivetrain.reset_gyro()

        if (self.controller.getLeftTriggerAxis() > 0.1) != (self.controller.getRightTriggerAxis() > 0.1):
            self.drivetrain.change_drivetrain_speed(0.75)
        elif self.controller.getLeftTriggerAxis() > 0.1 and self.controller.getRightTriggerAxis() > 0.1:
            self.drivetrain.change_drivetrain_speed(1)
        else:
            self.drivetrain.change_drivetrain_speed(0.5)

        if forward_speed > 0.2 or forward_speed < -0.2:
            self.forward_speed = forward_speed
        else:
            self.forward_speed = 0

        if strafe_speed > 0.2 or strafe_speed < -0.2:
            self.strafe_speed = strafe_speed
        else:
            self.strafe_speed = 0

        if rotation_speed > 0.2 or rotation_speed < -0.2:
            self.rotation_speed = rotation_speed
        else:
            self.rotation_speed = 0

        if self.joystick.getRawButtonPressed(5):
            self.shooter_state = "Reset"
        elif self.joystick.getRawButtonPressed(6):
            self.shooter_state = "Force Arm"
        elif self.joystick.getRawButtonPressed(7):
            self.shooter_state = "Drop Everything"

        match self.shooter_state:
            case "Idle":
                if self.joystick.getRawButtonPressed(2):
                    self.shooter.pick_up_note()
                    self.shooter_state = "Collecting"
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

        if self.forward_speed != 0 or self.strafe_speed != 0 or self.rotation_speed != 0:
            self.drivetrain.move_robot(self.forward_speed, self.strafe_speed, self.rotation_speed) 
        else:
            self.drivetrain.stop_robot()

if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
