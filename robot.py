import wpilib
from shooter import Shooter
from color_sensor import ColorSensor

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.joystick = wpilib.Joystick(0)
        self.shooter = Shooter()
        self.color_sensor = ColorSensor()

        self.timer = wpilib.Timer()
        self.shoot_timer = wpilib.Timer()

    def teleopInit(self):
        self.pick_up_note = False
        self.release_note = False
        self.fire_out_note = False
        self.has_ring = False
        self.shoot_primer = False
        self.timer.restart()
        self.shoot_timer.reset()

    def teleopPeriodic(self):
        if self.joystick.getRawButtonPressed(2):
            self.shooter.pick_up_note()
            self.pick_up_note = True

        if self.joystick.getRawButtonPressed(1):
            if self.shoot_primer == True:
                self.shoot_primer = False
                self.shooter.fire_out_note()
                self.fire_out_note = True
                self.shoot_timer.restart()
            else:
                self.shoot_primer = True
                self.shooter.prime_shooter()

        if self.pick_up_note == True:
            # if self.has_ring == True:
            #     self.shooter.release_note()
            #     self.release_note = True
            # else:
                if self.color_sensor.has_ring():
                    self.shooter.stop_picking_up_note()
                    self.pick_up_note = False
                    self.has_ring = True

        # if self.release_note == True:
        #     if not self.color_sensor.has_ring():
        #         self.shooter.stop_releasing_note()
        #         self.release_note = False

        if self.fire_out_note == True:
            if self.shoot_timer.hasElapsed(1):
                self.shooter.stop_firing_out_note()
                self.shoot_timer.stop()
                self.fire_out_note = False
            
if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
