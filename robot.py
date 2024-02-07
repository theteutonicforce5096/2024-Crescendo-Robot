import wpilib
import swerve_module
import math
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics, ChassisSpeeds
import time

class MyRobot(wpilib.TimedRobot):
    def robotInit(self) -> None:
        self.drivetrain = SwerveDrive()
        return super().robotInit()


    def teleopInit(self) -> None:
        self.joystick = wpilib.Joystick(0)
        self.timer = wpilib.Timer()
        self.timer.restart()
        self.drivetrain.teleopInit()
        self.last_dir = 0
        return super().teleopInit()
    
    
    def teleopPeriodic(self) -> None:
        rawX = self.joystick.getX()
        rawY = self.joystick.getY() * -1
        rotation = self.joystick.getZ() * -1
        # if mag < .1:
        #     mag = 0
        #     dir = self.last_dir
        # if mag > 1:
        #     mag = 1
        # self.last_dir = dir
        self.drivetrain.moveRobot(rawX, rawY, rotation)

        return super().teleopPeriodic()
    
    
class SwerveDrive:
    def __init__(self) -> None:
        pass

    def teleopInit(self) -> None:
        frontLeftLocation = Translation2d(0.3175, 0.3175)
        frontRightLocation = Translation2d(0.3175, -0.3175)
        backLeftLocation = Translation2d(-0.3175, 0.3175)
        backRightLocation = Translation2d(-0.3175, -0.3175)

        self.kinematics = SwerveDrive4Kinematics(
            frontLeftLocation, frontRightLocation, backLeftLocation, backRightLocation
        )
        
        self.FL_module = swerve_module.SwerveModule("FL", 23, 13, 33, -0.002686)
        self.FL_module.reset()

        self.FR_module = swerve_module.SwerveModule("FR", 20, 10, 30, 0.003906)
        self.FR_module.reset()

        self.BL_module = swerve_module.SwerveModule("BL", 22, 12, 32, -0.476807)
        self.BL_module.reset()

        self.BR_module = swerve_module.SwerveModule("BR", 21, 11, 31, 0.002930)
        self.BR_module.reset()

    def moveRobot(self, rawX, rawY, rotation):
        speeds = ChassisSpeeds(rawY, rawX, rotation)

        frontLeft, frontRight, backLeft, backRight = self.kinematics.desaturateWheelSpeeds(self.kinematics.toSwerveModuleStates(speeds), 1)
        print(frontRight.angle.degrees() + 360)
        self.FL_module.set_velocity(frontLeft.speed / 5, frontLeft.angle.degrees() + 360, 1)
        self.FR_module.set_velocity(frontRight.speed / 5, frontRight.angle.degrees() + 360, 1)
        self.BL_module.set_velocity(backLeft.speed / 5 , backLeft.angle.degrees() + 360, 1)
        self.BR_module.set_velocity(backRight.speed / 5, backRight.angle.degrees() + 360, 1)
        
if __name__ == "__main__":
    wpilib.run(MyRobot)