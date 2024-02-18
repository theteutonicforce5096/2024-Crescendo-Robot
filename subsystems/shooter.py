import wpilib
import phoenix6
import vision
import time
from robot import MyRobot

class Shooter():
    def __init__(self):
        self.shootMotor1 = phoenix6.hardware.TalonFX(1)
        self.shootMotor2 = phoenix6.hardware.TalonFX(2) # direction reverse
        self.elevationMotor1 = phoenix6.hardware.TalonFX(3)
        self.elevationMotor2 = phoenix6.hardware.TalonFX(4) # direction reverse
        self.intakeMotor = phoenix6.hardware.TalonFX(5)

    def align(self):
        pass
    
    def turnIntakeOn(self):
        self.intakeMotor.set_control(phoenix6.controls.DutyCycleOut(0.25))

    def turnIntakeOff(self):
        self.intakeMotor.set_control(phoenix6.controls.DutyCycleOut(0.0))

    def shoot(self, motorSpeed: int):
        """
        \"Hey Johnny, spin up those shooting motors!\"

        :param motorSpeed: Speed of the shooting motors. The higher, the further the ring goes 👀
        """
        if self.isReadyToShoot():
            self.shootMotor1.set_position(motorSpeed)
            self.shootMotor2.set_position()
        else:
            time.sleep(0.01)
            self.shoot()

    def isReadyToShoot(self) -> bool:
        if MyRobot.vision.hasRing():
            if self.shootMotor1.get_acceleration() == 0:
                return True
            else:
                return False
        else:
            return False
