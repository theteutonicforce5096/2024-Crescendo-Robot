import wpilib, phoenix5
from shooter import Shooter
from color_sensor import ColorSensor

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.joystick = wpilib.Joystick(0)
        self.shooter = Shooter()
        self.timer = wpilib.Timer()
        self.color_sensor = ColorSensor(wpilib.I2C.Port(3))

    def teleopInit(self):
        self.timer.restart()

    def teleopPeriodic(self):
        if self.joystick.getRawButtonPressed(11):
            self.shooter.move_arm_down()

        if self.joystick.getRawButtonPressed(12):
            self.shooter.move_arm_up()

if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
