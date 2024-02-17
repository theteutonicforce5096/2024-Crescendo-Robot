import wpilib
from drivetrain import SwerveDrive
from math import fabs

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.drivetrain = SwerveDrive()
        self.joystick = wpilib.Joystick(0)
        self.timer = wpilib.Timer()

    def teleopInit(self):
        self.forward_speed = 0
        self.strafe_speed = 0
        self.rotation_speed = 0
        self.stop_robot = False
        self.drivetrain.reset()
        self.timer.restart()
    
    def teleopPeriodic(self):
        magnitude = self.joystick.getMagnitude() 
        rotation_speed = self.joystick.getZ() * -1

        if magnitude > 0.2:
            self.forward_speed = self.joystick.getX() * -1
            self.strafe_speed = self.joystick.getY() * -1
        else:
            self.forward_speed = 0
            self.strafe_speed = 0

        if fabs(rotation_speed) > 0.2:
            self.rotation_speed = rotation_speed
        else:
            self.rotation_speed = 0

        if self.forward_speed != 0 or self.strafe_speed != 0 or self.rotation_speed != 0:
            self.drivetrain.move_robot(self.forward_speed, self.strafe_speed, rotation_speed) 
            self.stop_robot = False
        else:
            self.stop_robot = True

        if self.stop_robot:
            self.drivetrain.stop_robot()

if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
