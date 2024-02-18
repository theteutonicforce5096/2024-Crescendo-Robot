import wpilib
from drivetrain import SwerveDrive
from math import fabs

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.drivetrain = SwerveDrive()
        self.joystick = wpilib.Joystick(0)
        self.timer = wpilib.Timer()

    def teleopInit(self):
        # Default speeds
        self.forward_speed = 0
        self.strafe_speed = 0
        self.rotation_speed = 0

        # Reset drivetrain and timer
        self.drivetrain.reset()
        self.timer.restart()
    
    def teleopPeriodic(self):
        print(round(self.drivetrain.get_current_robot_angle(), 2))
        magnitude = self.joystick.getMagnitude() 
        rotation_speed = self.joystick.getZ()

        if magnitude > 0.2:
            self.forward_speed = self.joystick.getX()
            self.strafe_speed = self.joystick.getY() 
        else:
            self.forward_speed = 0
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

if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
