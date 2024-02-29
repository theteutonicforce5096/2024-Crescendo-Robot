import wpilib
from arm import Arm

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Initialize components
        self.arm = Arm(50, 51, True, False, 0)

        # Initialize controllers
        self.controller = wpilib.XboxController(0)

        # Initialize timer
        self.timer = wpilib.Timer()

    def teleopInit(self):
        # Reset timers
        self.timer.restart()

        # Reset Arm
        self.arm.reset()

    def teleopPeriodic(self):
        if self.controller.getAButtonPressed():
            self.arm.set(0)
        elif self.controller.getBButtonPressed():
            self.arm.set(30)
        elif self.controller.getXButtonPressed():
            self.arm.set(60)
        elif self.controller.getYButtonPressed():
            self.arm.set(90)

        self.arm.update_pid_controller() 

if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
