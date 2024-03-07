import wpilib
from arm import Arm
import phoenix6

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Initialize components
        self.arm = Arm(50, 51, True, False, 0, 0.9853633496340838, 0.9550960488774012)
        self.controller = wpilib.XboxController(0)

    def teleopInit(self):
        self.arm.reset()

    def teleopPeriodic(self):
        print(self.arm._get_encoder_value())
        if self.controller.getAButtonPressed():
            self.arm.set(0)
        elif self.controller.getBButtonPressed():
            self.arm.set(45)
        elif self.controller.getYButtonPressed():
            self.arm.set(80)
        self.arm.update_pid_controller()

if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
