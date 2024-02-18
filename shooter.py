import phoenix5

class Shooter():
    def __init__(self):
        self.intake_motor = phoenix5.VictorSPX(9)
        self.shoot_left_motor = phoenix5.VictorSPX(8)
        self.shoot_right_motor = phoenix5.VictorSPX(6)
        self.arm_left = phoenix5.VictorSPX(10)
        self.arm_right = phoenix5.VictorSPX(31)

    def pick_up_note(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, 0.5)

    def stop_picking_up_note(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, 0)

    def release_note(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, -0.5)

    def stop_releasing_note(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, 0)

    def prime_shooter(self):
        self.shoot_left_motor.set(phoenix5.ControlMode.PercentOutput, 0.6)
        self.shoot_right_motor.set(phoenix5.ControlMode.PercentOutput, 0.6)
    
    def fire_out_note(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, 0.5)

    def stop_firing_out_note(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, 0)
        self.shoot_left_motor.set(phoenix5.ControlMode.PercentOutput, 0)
        self.shoot_right_motor.set(phoenix5.ControlMode.PercentOutput, 0)

    def move_arm_up(self):
        self.arm_left.set(phoenix5.ControlMode.PercentOutput, -0.6)
        self.arm_right.set(phoenix5.ControlMode.PercentOutput, 0.6)

    def move_arm_down(self):
        self.arm_left.set(phoenix5.ControlMode.PercentOutput, 0.6)
        self.arm_right.set(phoenix5.ControlMode.PercentOutput, -0.6)

    def stop_arm(self):
        self.arm_left.set(phoenix5.ControlMode.PercentOutput, 0)
        self.arm_right.set(phoenix5.ControlMode.PercentOutput, 0)