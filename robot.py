import wpilib
import swerve_module


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
        if self.timer.advanceIfElapsed(.3):
            self.drivetrain.moveRobot(mag, dir)

            
        return super().teleopPeriodic()
    
    
class SwerveDrive:
    def __init__(self) -> None:
        pass

    def teleopInit(self) -> None:
        self.BR_module = swerve_module.SwerveModule("BR", 21, 11, 31, 0, .5)
        self.BR_module.reset()
        self.BL_module = swerve_module.SwerveModule("BL", 21, 11, 31, 0, .5)
        self.BL_module.reset()
        self.FR_module = swerve_module.SwerveModule("FR", 21, 11, 31, 0, .5)
        self.FR_module.reset()
        self.FL_module = swerve_module.SwerveModule("FL", 21, 11, 31, 0, .5)
        self.FL_module.reset()

    def moveRobot(self, mag, dir):
        #print ("Direction is: " + str(round(dir,3)) + "    Magnitude is: " + str(round(mag,3)))
        self.BR_module.set_velocity(mag, dir, 1)
        self.BL_module.set_velocity(mag, dir, 1)
        self.FR_module.set_velocity(mag, dir, 1)
        self.FL_module.set_velocity(mag, dir, 1)
    

    

if __name__ == "__main__":
    wpilib.run(MyRobot)