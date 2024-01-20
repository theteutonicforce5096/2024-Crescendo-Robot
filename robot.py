import wpilib
import wpilib.drive
import ctre
import os
import ntcore
import robotpy_apriltag
from cscore import CameraServer
from magicbot import MagicRobot
from robotpy_ext.autonomous.selector import AutonomousModeSelector
import autonomous
from rev import ColorSensorV3

class MyRobot(MagicRobot):

    def createObjects(self):
        pass

    def teleopInit(self):
        self.colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)
        #self.colorSensor.configureProximitySensorLED(current=ColorSensorV3.LEDCurrent.kPulse5mA)

    def teleopPeriodic(self):
        detectColor = self.colorSensor.getColor()
        #print(detectColor)
        proximity = self.colorSensor.getProximity()
        wpilib.SmartDashboard.putNumber("Proximity", proximity)
        #print(proximity)
        rawDetectColor = self.colorSensor.getRawColor()
        wpilib.SmartDashboard.putNumber("Raw Red", rawDetectColor.red)
        wpilib.SmartDashboard.putNumber("Raw Green", rawDetectColor.green)
        wpilib.SmartDashboard.putNumber("Raw Blue", rawDetectColor.blue)
        #print("red", rawDetectColor.red)
        #print("green", rawDetectColor.green)
        #print("blue", rawDetectColor.blue)
    
    def autonomousInit(self):
        pass

    def autonomous(self):
        # For auto, use MagicBot's auto mode.
        # This will load the ./autonomous folder.
        super().autonomous()

if __name__ == '__main__':
    wpilib.run(MyRobot)