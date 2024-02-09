import wpilib
from drivetrain import SwerveDrive
from math import fabs

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.drivetrain = SwerveDrive()
        self.joystick = wpilib.Joystick(0)
        self.timer = wpilib.Timer()

    def teleopInit(self):
        self.raw_x = 0
        self.raw_y = 0
        self.rotation = 0
        self.drivetrain.reset()
        self.timer.restart()
    
    def teleopPeriodic(self):
        magnitude = self.joystick.getMagnitude() 
        rotation = self.joystick.getZ() * -1
        if magnitude > 0.2:
            self.raw_x = self.joystick.getX() * -1
            self.raw_y = self.joystick.getY() * -1
        else:
            self.raw_x = 0
            self.raw_y = 0

        if fabs(rotation) > 0.2:
            self.rotation = rotation
        else:
            self.rotation = 0

        if self.raw_x != 0 or self.raw_y != 0 or self.rotation != 0:
            self.drivetrain.move_robot(self.raw_x, self.raw_y, rotation) 
        else:
            self.drivetrain.stop_robot()

if __name__ == "__main__":
    wpilib.run(MyRobot)
