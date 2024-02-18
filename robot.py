import wpilib
from shooter import Shooter
from color_sensor import ColorSensor
from drivetrain import SwerveDrive
from math import fabs

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.joystick = wpilib.Joystick(0)
        self.controller = wpilib.XboxController(1)
        self.shooter = Shooter()
        self.drivetrain = SwerveDrive()
        self.color_sensor = ColorSensor()

        self.timer = wpilib.Timer()
        self.shoot_timer = wpilib.Timer()
        self.cancel_intake_timer = wpilib.Timer()

    def teleopInit(self):
        # Default speeds
        self.forward_speed = 0
        self.strafe_speed = 0
        self.rotation_speed = 0

        self.drivetrain.reset()
        self.shooter.reset()
        
        self.shooter_state = "Idle"
        
        self.timer.restart()
        self.shoot_timer.reset()
        self.cancel_intake_timer.reset()

    def teleopPeriodic(self):
        self.color_sensor.has_ring()
        forward_speed = self.joystick.getX()
        strafe_speed = self.joystick.getY()
        rotation_speed = self.joystick.getZ()

        if forward_speed > 0.1:
            self.forward_speed = forward_speed
        else:
            self.forward_speed = 0

        if forward_speed > 0.1:
            self.strafe_speed = strafe_speed
        else:
            self.strafe_speed = 0

        if fabs(rotation_speed) > 0.2:
            self.rotation_speed = rotation_speed 
        else:
            self.rotation_speed = 0

        if self.forward_speed != 0 or self.strafe_speed != 0 or self.rotation_speed != 0:
            self.drivetrain.move_robot(self.forward_speed, self.strafe_speed, rotation_speed) 
        else:
            self.drivetrain.stop_robot()

        if self.joystick.getRawButtonPressed(12):
            self.drivetrain.gyro.reset()
        
        match self.shooter_state:
            case "Idle":
                if self.controller.getAButtonPressed():
                    self.shooter.pick_up_note()
                    self.shooter_state = "Collecting"
            case "Collecting":
                if self.color_sensor.has_ring():
                    self.shooter.stop_picking_up_note()
                    self.shooter_state = "Load"
                
                if self.controller.getYButtonPressed():
                    self.shooter.release_note()
                    self.cancel_intake_timer.restart()

                if self.cancel_intake_timer.hasElapsed(0.1):
                    self.shooter.stop_releasing_note()
                    self.cancel_intake_timer.reset()
                    self.shooter_state = "Load"
            case "Load":
                if self.joystick.getRawButtonPressed(1):
                    self.shooter.prime_shooter()
                    self.shoot_timer.restart()
                    self.shooter_state = "Arm"
            #     elif self.joystick.getRawButtonPressed(2):
            #         self.shooter.release_note()
            #         self.shooter_state = "Releasing"
            # case "Releasing":
            #     if not self.color_sensor.has_ring():
            #         self.shooter.stop_releasing_note()
            #         self.shooter_state = "Idle"
            case "Arm":
                if self.shoot_timer.hasElapsed(2.5):
                    if self.joystick.getRawButtonPressed(1):
                        self.shooter.fire_out_note()
                        self.shoot_timer.restart()
                        self.shooter_state = "Fire"
            case "Fire":
                if self.shoot_timer.hasElapsed(0.5):
                    self.shooter.stop_firing_out_note()
                    self.shoot_timer.reset()
                    self.shooter_state = "Idle"
            
if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
