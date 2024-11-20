import wpilib
import wpilib.drive

class TheRinger(wpilib.TimedRobot):
    def robotInit(self):
        # Replace motor_id with device number of each motor
        # Replace joystick_id with USB port number of joystick
        self.front_left = wpilib.PWMVictorSPX(motor_id)
        self.rear_left = wpilib.PWMVictorSPX(motor_id)
        self.left = wpilib.MotorControllerGroup(self.front_left, self.rear_left)

        self.front_right = wpilib.PWMVictorSPX(motor_id)
        self.rear_right = wpilib.PWMVictorSPX(motor_id)
        self.right = wpilib.MotorControllerGroup(self.front_right, self.rear_right)

        self.drivetrain = wpilib.drive.DifferentialDrive(self.left, self.right)

        self.joystick = wpilib.Joystick(joystick_id)

    def teleopPeriodic(self):
        # Make sure that the joysticks Y value increasing when moving forward and decreases when moving backwards
        forward_speed = self.joystick.getY()
        self.drivetrain.arcadeDrive(-self.driveStick.getY(), -self.driveStick.getX())

        
if __name__ == "__main__":
    wpilib.run(TheRinger)