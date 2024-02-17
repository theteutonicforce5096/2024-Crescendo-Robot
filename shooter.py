import phoenix5

class Shooter():
    def __init__(self):
        self.intake_motor = phoenix5.VictorSPX(9)
        self.shoot_left_motor = phoenix5.VictorSPX(8)
        self.shoot_right_motor = phoenix5.VictorSPX(6)
        self.arm_left = phoenix5.VictorSPX(10)
        self.arm_right = phoenix5.VictorSPX(31)

    def pick_up_note(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, 0.2)

    def stop_picking_up_note(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, 0)

    def release_note(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, -0.2)

    def stop_releasing_note(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, 0)

    def fire_out_note(self):
        self.shoot_left_motor.set(phoenix5.ControlMode.PercentOutput, 0.2)
        self.shoot_right_motor.set(phoenix5.ControlMode.PercentOutput, 0.2)

    def stop_firing_out_note(self):
        self.shoot_left_motor.set(phoenix5.ControlMode.PercentOutput, 0)
        self.shoot_right_motor.set(phoenix5.ControlMode.PercentOutput, 0)

    def move_arm_up(self):
        self.arm_left.set(phoenix5.ControlMode.PercentOutput, -0.6)
        self.arm_right.set(phoenix5.ControlMode.PercentOutput, 0.6)

    def move_arm_down(self):
        self.arm_left.set(phoenix5.ControlMode.PercentOutput, 0.6)
        self.arm_right.set(phoenix5.ControlMode.PercentOutput, -0.6)

    # def shoot(self, motorSpeed: int):
    #     """
    #     \"Hey Johnny, spin up those shooting motors!\"

    #     :param motorSpeed: Speed of the shooting motors. The higher, the further the ring goes 👀
    #     """
    #     if self.isReadyToShoot():
    #         self.shootMotor1.set_position(motorSpeed)
    #         self.shootMotor2.set_position()
    #     else:
    #         time.sleep(0.01)
    #         self.shoot()

    # def isReadyToShoot(self) -> bool:
    #     if vision.Vision().hasRing():
    #         if self.shootMotor1.get_acceleration() == 0:
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False
