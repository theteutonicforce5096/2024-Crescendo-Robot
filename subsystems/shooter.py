import wpilib
import phoenix6
import vision
import time

class Shooter():
    def __init__(self):
        self.shootMotor1 = phoenix6.hardware.TalonFX(1)
        self.shootMotor2 = phoenix6.hardware.TalonFX(2)

    def align(self):
        pass
    
    def shoot(self, motorSpeed: int):
        """
        \"Hey Johnny, spin up those shooting motors!\"

        :param motorSpeed: Speed of the shooting motors. The higher, the further the ring goes 👀
        """
        if self.isReadyToShoot():
            self.shootMotor1.set_position(motorSpeed)
            self.shootMotor2.set_position(motorSpeed)
        else:
            time.sleep(0.01)
            self.shoot()

    def isReadyToShoot(self) -> bool:
        if vision.Vision().hasRing():
            if self.shootMotor1.get_acceleration() == 0:
                return True
            else:
                return False
        else:
            return False
