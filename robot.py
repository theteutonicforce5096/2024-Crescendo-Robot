# TODO: insert robot code here
import wpilib
import math



class MyRobot(wpilib.TimedRobot):
    def teleopInit(self) -> None:
        self.joystick=wpilib.Joystick()
        self.timer=wpilib.Timer()
        self.timer.restart()
        return super().teleopInit()
    
    
    def teleopPeriodic(self) -> None:
        if self.timer.advanceIfElapsed(.5):
            dir = self.joystick.getDirectionDegrees()
            mag = self.joystick.getMagnitude()
            print ("Direction is: " + dir + "    Magnitude is: " + mag)
        
        return super().teleopPeriodic()
    
    
class SwerveDrive:
    def moveRobot(speed, direction):
        pass

class SwerveModuleStub:
    def driveModule(speed, direction):
        print("Speed is: " + str(speed) + "    Direction is: " + str(direction))
    

if __name__ == "__main__":
    wpilib.run(MyRobot)