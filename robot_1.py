import wpilib, phoenix5
from shooter import Shooter

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.joystick = wpilib.Joystick(0)
        self.shooter = Shooter()
        self.timer = wpilib.Timer()

    def teleopInit(self):
        self.intaking_note = False
        self.outtaking_note = False
        self.has_note = False
        self.timer.restart()
        self.shoot_timer.reset()

    def teleopPeriodic(self):
        if self.shoot_timer.hasElapsed(1):
            self.shoot_motor.set_control(phoenix6.controls.DutyCycleOut(0))
            self.has_note = False

        if self.joystick.getRawButton(2):
            if self.has_note == False:
                self.intake_motor.set_control(phoenix6.controls.DutyCycleOut(0.2))
                self.intaking_note = True
            elif self.has_note: 
                self.intake_motor.set_control(phoenix6.controls.DutyCycleOut(-0.2))
                self.outtaking_note = True
        elif self.joystick.getRawButton(1):
            if self.has_note:
                self.shoot_motor.set_control(phoenix6.controls.DutyCycleOut(0.2))
                self.shoot_timer.restart()

        loaded_note = self.color_sensor.get()

        if loaded_note and self.intaking_note == True:
            self.intake_motor.set_control(phoenix6.controls.DutyCycleOut(0))
            self.intaking_note = False
            self.has_note = True
        elif loaded_note == False and self.outtaking_note == True:
            self.intake_motor.set_control(phoenix6.controls.DutyCycleOut(0))
            self.outtaking_note = False
            self.has_note = False

if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
