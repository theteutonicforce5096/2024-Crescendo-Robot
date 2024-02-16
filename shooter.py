import phoenix6
from wpilib import DigitalInput 

class Shooter():
    def __init__(self):
        self.intake_motor = phoenix6.hardware.TalonFX(5)
        self.shoot_motor_1 = phoenix6.hardware.TalonFX(1)
        self.shoot_motor_2 = phoenix6.hardware.TalonFX(2) 
        self.arm_motor_1 = phoenix6.hardware.TalonFX(3)
        self.arm_motor_2 = phoenix6.hardware.TalonFX(4) 
        self.color_sensor = DigitalInput(0) # TODO: Change to real color sensor

        # PID Configs
        self.set_pid(self.intake_motor, 0, 0, 0, 0, 0)
        self.set_pid(self.shoot_motor_1, 0, 0, 0, 0, 0)
        self.set_pid(self.shoot_motor_2, 0, 0, 0, 0, 0)
        self.set_pid(self.arm_motor_1, 0, 0, 0, 0, 0)
        self.set_pid(self.arm_motor_2, 0, 0, 0, 0, 0)

        # PID
        self.intake_motor_pid = phoenix6.controls.VelocityVoltage(velocity = 0, enable_foc = False)
        self.shoot_motor_1_pid = phoenix6.controls.VelocityVoltage(velocity = 0, enable_foc = False)
        self.shoot_motor_2_pid = phoenix6.controls.VelocityVoltage(velocity = 0, enable_foc = False)
        self.arm_motor_1_pid = phoenix6.controls.VelocityVoltage(velocity = 0, enable_foc = False)
        self.arm_motor_2_pid = phoenix6.controls.VelocityVoltage(velocity = 0, enable_foc = False)

    def set_pid(self, motor, s, v, p, i, d):
        # PID Configs
        self.talonfx_configs = phoenix6.configs.TalonFXConfiguration()
        self.talonfx_configs.slot0.k_s = s
        self.talonfx_configs.slot0.k_v = v
        self.talonfx_configs.slot0.k_p = p
        self.talonfx_configs.slot0.k_i = i
        self.talonfx_configs.slot0.k_d = d

        motor.configurator.apply(self.talonfx_configs) 

    def intake_note(self):
        self.intake_motor.set_control(self.intake_motor_pid.with_velocity(8))
        

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
        if vision.Vision().hasRing():
            if self.shootMotor1.get_acceleration() == 0:
                return True
            else:
                return False
        else:
            return False
