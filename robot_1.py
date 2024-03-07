import wpilib
from arm import Arm
from vision import Vision

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Initialize components
        self.arm = Arm(50, 51, True, False, 0, 0.1793784294844607, 0.138)

    def teleopPeriodic(self):
        print(self.arm._get_encoder_value())

if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
