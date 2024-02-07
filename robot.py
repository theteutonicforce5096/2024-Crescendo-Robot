import wpilib
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics, ChassisSpeeds
from swerve_module import SwerveModule
import math

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        #super().robotInit()
        self.drivetrain = SwerveDrive()

    def teleopInit(self):
        self.joystick = wpilib.Joystick(0)
        self.timer = wpilib.Timer()
        self.timer.restart()
    
    def teleopPeriodic(self):
        raw_x = self.joystick.getX()
        raw_y = self.joystick.getY() * -1
        rotation = self.joystick.getZ() * -1 * math.pi
        magnitude = self.joystick. # Get Magnitude function
        if magnitude > 0.2:
            self.drivetrain.move_robot(raw_x, raw_y, rotation)    
    
class SwerveDrive:
    def __init__(self):
        FL_location = Translation2d(0.3175, 0.3175)
        FR_location = Translation2d(0.3175, -0.3175)
        BL_location = Translation2d(-0.3175, 0.3175)
        BR_location = Translation2d(-0.3175, -0.3175)

        self.kinematics = SwerveDrive4Kinematics(FL_location, FR_location, BL_location, BR_location)
        
        self.FL_module = SwerveModule("FL", 23, 13, 33, -0.002686)
        self.FL_module.reset()

        self.FR_module = SwerveModule("FR", 20, 10, 30, 0.003906)
        self.FR_module.reset()

        self.BL_module = SwerveModule("BL", 22, 12, 32, -0.476807)
        self.BL_module.reset()

        self.BR_module = SwerveModule("BR", 21, 11, 31, 0.002930)
        self.BR_module.reset()

    def move_robot(self, raw_x, raw_y, rotation):
        speeds = ChassisSpeeds(raw_x, raw_y, rotation)
        FL_state, FR_state, BL_state, BR_state = self.kinematics.desaturateWheelSpeeds(self.kinematics.toSwerveModuleStates(speeds), 1)

        self.FL_module.set_velocity(FL_state.speed / 5, FL_state.angle.degrees(), 1)
        self.FR_module.set_velocity(FR_state.speed / 5, FR_state.angle.degrees(), 1)
        self.BL_module.set_velocity(BL_state.speed / 5 , BL_state.angle.degrees(), 1)
        self.BR_module.set_velocity(BR_state.speed / 5, BR_state.angle.degrees(), 1)
        
if __name__ == "__main__":
    wpilib.run(MyRobot)
