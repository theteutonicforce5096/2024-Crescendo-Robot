import wpilib, phoenix5
from shooter import Shooter
from color_sensor import ColorSensor

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.joystick = wpilib.Joystick(0)
        self.shooter = Shooter()
        self.timer = wpilib.Timer()
        self.color_sensor = ColorSensor()

    def teleopInit(self):
        self.pick_up_note = False
        self.release_note = False
        self.has_ring = False
        self.timer.restart()

    def teleopPeriodic(self):
        if self.joystick.getRawButtonPressed(2):
            self.shooter.pick_up_note()
            self.pick_up_note = True

        if self.pick_up_note == True:
            if self.has_ring == True:
                self.shooter.release_note()
                self.release_note = True
            if self.color_sensor.has_ring():
                self.shooter.stop_picking_up_note()
                self.pick_up_note = False
                self.has_ring = True

        if self.release_note == True:
            if not self.color_sensor.has_ring():
                self.shooter.stop_releasing_note()
                self.release_note = False
            


if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
