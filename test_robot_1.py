import wpilib
from arm import Arm
import phoenix6
from drivetrain import SwerveDrive
from shooter import Shooter

class TeutonicForceRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Initialize components
        #self.arm = Arm(51, 50, True, False, 0, 0, 0, 0)
        self.drivetrain = SwerveDrive()
        self.shooter = Shooter(40, 41, 42, False, False, False)

        # Initialize controllers
        self.drivetrain_controller = wpilib.XboxController(0)
        self.controller = wpilib.XboxController(1)

        self.right_motor = phoenix6.hardware.TalonFX(51)
        self.left_motor = phoenix6.hardware.TalonFX(50)

        # Initialize timer
        self.timer = wpilib.Timer()

        # Set default robot speeds
        self.forward_speed = 0
        self.strafe_speed = 0
        self.rotation_speed = 0

    def teleopInit(self):
        # Reset timers
        self.timer.restart()

        # Reset robot speeds.
        self.forward_speed = 0
        self.strafe_speed = 0
        self.rotation_speed = 0

        # Reset Drivetrain
        self.drivetrain.reset_drivetrain()
        self.drivetrain.reset_gyro()

        # Enable Drivetrain
        self.drivetrain.change_drivetrain_state("Enabled")

    def teleopPeriodic(self):
        # if self.controller.getAButtonPressed():
        #     self.arm.set(0)
        # elif self.controller.getBButtonPressed():
        #     self.arm.set(30)
        # elif self.controller.getXButtonPressed():
        #     self.arm.set(45)
        # elif self.controller.getLeftBumperPressed():
        #     self.arm.set(60)
        # elif self.controller.getYButtonPressed():
        #     self.arm.set(90)

        # self.arm.update_pid_controller() 

        if self.controller.getAButtonPressed():
            # Forward
            self.right_motor.set_control(phoenix6.controls.DutyCycleOut(0.25))
            self.left_motor.set_control(phoenix6.controls.DutyCycleOut(-0.25))
        elif self.controller.getBButtonPressed():
            # Backward
            self.right_motor.set_control(phoenix6.controls.DutyCycleOut(-0.25))
            self.left_motor.set_control(phoenix6.controls.DutyCycleOut(0.25))
        elif self.controller.getXButtonPressed():
            self.right_motor.set_control(phoenix6.controls.DutyCycleOut(0))
            self.left_motor.set_control(phoenix6.controls.DutyCycleOut(0))

        # Get speeds from drivetrain controller.
        forward_speed = self.drivetrain_controller.getLeftY()
        strafe_speed = self.drivetrain_controller.getLeftX()
        rotation_speed = self.drivetrain_controller.getRightX()

        # Check if max drivetrain speed needs to be changed.
        if (self.drivetrain_controller.getLeftTriggerAxis() > 0.1) != (self.drivetrain_controller.getRightTriggerAxis() > 0.1):
            self.drivetrain.change_max_drivetrain_speed(0.75)
        elif self.drivetrain_controller.getLeftTriggerAxis() > 0.1 and self.drivetrain_controller.getRightTriggerAxis() > 0.1:
            self.drivetrain.change_max_drivetrain_speed(1.0)
        else:
            self.drivetrain.change_max_drivetrain_speed(0.5)

        # Set deadzone on forward speed.
        if forward_speed > 0.1 or forward_speed < -0.1:
            self.forward_speed = forward_speed
        else:
            self.forward_speed = 0

        # Set deadzone on strafe speed.
        if strafe_speed > 0.1 or strafe_speed < -0.1:
            self.strafe_speed = strafe_speed
        else:
            self.strafe_speed = 0

        # Set deadzone on rotation speed.
        if rotation_speed > 0.1 or rotation_speed < -0.1:
            self.rotation_speed = rotation_speed
        else:
            self.rotation_speed = 0

        # Move robot if drivetrain is enabled.
        match self.drivetrain.get_drivetrain_state():
            case "Enabled":
                if self.forward_speed != 0 or self.strafe_speed != 0 or self.rotation_speed != 0:
                    self.drivetrain.move_robot(self.forward_speed, self.strafe_speed, self.rotation_speed) 
                else:
                    self.drivetrain.stop_robot()

if __name__ == "__main__":
    wpilib.run(TeutonicForceRobot)
