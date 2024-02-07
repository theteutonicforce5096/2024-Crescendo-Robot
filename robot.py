import wpilib
import swerve_module
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics, ChassisSpeeds


class MyRobot(wpilib.TimedRobot):
    def robotInit(self) -> None:
        self.drivetrain = SwerveDrive()
        return super().robotInit()


    def teleopInit(self) -> None:
        self.joystick=wpilib.Joystick(0)
        self.timer=wpilib.Timer()
        self.timer.restart()
        self.drivetrain.teleopInit()
        self.last_dir = 0
        return super().teleopInit()
    
    
    def teleopPeriodic(self) -> None:
        dir = self.joystick.getDirectionDegrees()
        mag = self.joystick.getMagnitude()
        if mag < .1:
            mag = 0
            dir = self.last_dir
        if mag > 1:
            mag = 1
        self.last_dir = dir
        self.drivetrain.moveRobot(mag, dir)

            
        return super().teleopPeriodic()
    
    
class SwerveDrive:
    def __init__(self) -> None:
        pass

    def teleopInit(self) -> None:
        frontLeftLocation = Translation2d(0.381, 0.381)
        frontRightLocation = Translation2d(0.381, -0.381)
        backLeftLocation = Translation2d(-0.381, 0.381)
        backRightLocation = Translation2d(-0.381, -0.381)

        self.kinematics = SwerveDrive4Kinematics(
            frontLeftLocation, frontRightLocation, backLeftLocation, backRightLocation
        )

        self.BR_module = swerve_module.SwerveModule("BR", 21, 11, 31, 0.002930)
        self.BR_module.reset()

        self.BL_module = swerve_module.SwerveModule("BL", 22, 12, 32, -0.476807)
        self.BL_module.reset()

        self.FR_module = swerve_module.SwerveModule("FR", 20, 10, 30, 0.003906)
        self.FR_module.reset()

        self.FL_module = swerve_module.SwerveModule("FL", 23, 13, 33, -0.002686)
        self.FL_module.reset()

    def moveRobot(self, mag, dir):

        # speeds = ChassisSpeeds(, , 1.5)

        # frontLeft, frontRight, backLeft, backRight = self.kinematics.toSwerveModuleStates(speeds)

        self.BR_module.set_velocity(mag, dir, 1)

        self.BL_module.set_velocity(mag, dir, 1)

        self.FR_module.set_velocity(mag, dir, 1)

        self.FL_module.set_velocity(mag, dir, 1)
    

    

if __name__ == "__main__":
    wpilib.run(MyRobot)