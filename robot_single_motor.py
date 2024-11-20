import wpilib

class TheRinger(wpilib.TimedRobot):
    def robotInit(self):
        # Replace motor_id with device number of motor
        # Replace joystick_id with USB port number of joystick
        self.motor = wpilib.PWMVictorSPX(motor_id)

        self.joystick = wpilib.Joystick(joystick_id)

    def teleopPeriodic(self):
        # Make sure that the joysticks Y value increasing when moving forward and decreases when moving backwards
        forward_speed = self.joystick.getY()
        self.motor.set(forward_speed)
        
if __name__ == "__main__":
    wpilib.run(TheRinger)