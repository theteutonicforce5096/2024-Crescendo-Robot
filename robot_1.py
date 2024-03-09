import wpilib
from wpilib.shuffleboard import Shuffleboard
from subsystems.drivetrain import SwerveDrive
from subsystems.arm import Arm

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Initialize components
        self.drivetrain = SwerveDrive()
        self.arm = Arm(50, 51, True, False, 0, 0.9853633496340838, 0.9550960488774012)
        self.drivetrain.reset_drivetrain()

        # Initialize controllers
        self.drivetrain_controller = wpilib.XboxController(0)

        # Initialize timers
        self.timer = wpilib.Timer()

        self.v_widget = Shuffleboard.getTab("PID").add(f"Voltage", 0.0).withSize(2, 2).getEntry()

        self.voltage = 0.0

    def teleopInit(self):
        # Reset timers
        self.timer.restart()
        self.voltage = 0.0

    def teleopPeriodic(self):
        # if self.drivetrain_controller.getYButtonPressed():
        #     self.voltage += 1
        # elif self.drivetrain_controller.getAButtonPressed():
        #     self.voltage -= 1
        
        # self.drivetrain.set_voltage(self.voltage)

        if self.drivetrain_controller.getYButtonPressed():
            self.voltage += 0.01
        elif self.drivetrain_controller.getAButtonPressed():
            self.voltage -= 0.01
        
        self.arm.set_voltage(self.voltage)
        self.v_widget.setFloat(self.voltage)

