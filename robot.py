import wpilib
from subsystems.drivetrain import SwerveDrive
#from subsystems.arm import Arm

class TheRinger(wpilib.TimedRobot):
    def robotInit(self):
        # Set brownout voltage
        wpilib.RobotController.setBrownoutVoltage(6.3)

        # Initialize components
        self.drivetrain = SwerveDrive(8.2296, 4.105, 90)
        #self.arm = Arm(50, 51, True, False, 0, 0.9960985499024637)

        # Initialize controllers
        self.drivetrain_controller = wpilib.XboxController(0)
        #self.shooter_controller = wpilib.XboxController(1)

        # Initialize timers
        self.timer = wpilib.Timer()
        self.drivetrain_timer = wpilib.Timer()

        # Set default robot speeds
        self.forward_speed = 0
        self.strafe_speed = 0
        self.rotation_speed = 0

    def teleopInit(self):
        # Reset timers
        self.timer.restart()
        self.drivetrain_timer.reset()

        # Reset Drivetrain
        self.drivetrain.reset_drivetrain()
        self.drivetrain.reset_gyro()
            
        # Reset Arm
        #self.arm.reset()

    def teleopPeriodic(self):
        # Get speeds from drivetrain controller.
        forward_speed = self.drivetrain_controller.getLeftY()
        strafe_speed = self.drivetrain_controller.getLeftX()
        rotation_speed = self.drivetrain_controller.getRightX()
        
        # Check if gyro needs to be reset.
        if self.drivetrain_controller.getAButtonPressed() and self.drivetrain_controller.getLeftBumperPressed() and self.drivetrain_controller.getRightBumperPressed():
            self.drivetrain.stop_robot()
            self.drivetrain.reset_gyro()
            self.drivetrain_timer.restart()
            self.drivetrain.change_drivetrain_state("Resetting Gyro")
        
        # Check if max drivetrain speed needs to be changed.
        if self.drivetrain_controller.getLeftTriggerAxis() > 0.1 and self.drivetrain_controller.getRightTriggerAxis() > 0.1:
            self.drivetrain.change_max_drivetrain_speed(1.0)
        elif self.drivetrain_controller.getLeftTriggerAxis() > 0.1:
            self.drivetrain.change_max_drivetrain_speed(0.5)
        elif self.drivetrain_controller.getRightTriggerAxis() > 0.1:
            self.drivetrain.change_max_drivetrain_speed(0.75)
        else:
            self.drivetrain.change_max_drivetrain_speed(0.25)

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

        # Check for arm setpoint change
        # pov = self.shooter_controller.getPOV()
        # if pov == 0:
        #     self.arm.set(self.arm.get_arm_setpoint() + 0.5)
        # elif pov == 180:
        #     self.arm.set(self.arm.get_arm_setpoint() - 0.5)

        # # Update arm position
        # self.arm.update_pid_controller() 

        # Update odometry
        pose = self.drivetrain.update_odometry()

        # Evaluate drivetrain state.
        match self.drivetrain.get_drivetrain_state():
            case "Enabled":
                if self.forward_speed != 0 or self.strafe_speed != 0 or self.rotation_speed != 0:
                    self.drivetrain.move_robot(self.forward_speed, self.strafe_speed, self.rotation_speed) 
                else:
                    self.drivetrain.stop_robot()
            case "Resetting Gyro":
                if not self.drivetrain_timer.hasElapsed(0.5):
                    if self.forward_speed != 0 or self.strafe_speed != 0 or self.rotation_speed != 0:
                        self.drivetrain_controller.setRumble(wpilib.XboxController.RumbleType.kBothRumble, 0.75)  
                    else:
                        self.drivetrain_controller.setRumble(wpilib.XboxController.RumbleType.kBothRumble, 0)  
                else:
                    self.drivetrain_controller.setRumble(wpilib.XboxController.RumbleType.kBothRumble, 0)  
                    self.drivetrain_timer.reset()
                    self.drivetrain.change_drivetrain_state("Enabled")
            case "Disabled":
                if self.forward_speed != 0 or self.strafe_speed != 0 or self.rotation_speed != 0:
                    self.drivetrain_controller.setRumble(wpilib.XboxController.RumbleType.kBothRumble, 0.75)
                else:
                    self.drivetrain_controller.setRumble(wpilib.XboxController.RumbleType.kBothRumble, 0)
                    
    def teleopExit(self):
        # Turn off drivetrain controller rumble if it is stil on.
        self.drivetrain_controller.setRumble(wpilib.XboxController.RumbleType.kBothRumble, 0)  

if __name__ == "__main__":
    wpilib.run(TheRinger)