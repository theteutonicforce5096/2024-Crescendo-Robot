import phoenix5
from wpilib.shuffleboard import Shuffleboard

class Shooter():
    def __init__(self, intake_motor_id, shooter_left_motor_id, shooter_right_motor_id, arm_left_motor_id, arm_right_motor_id):
        self.intake_motor = phoenix5.VictorSPX(intake_motor_id)
        self.shooter_left_motor = phoenix5.VictorSPX(shooter_left_motor_id)
        self.shooter_right_motor = phoenix5.VictorSPX(shooter_right_motor_id)
        self.arm_left_motor = phoenix5.VictorSPX(arm_left_motor_id)
        self.arm_right_motor = phoenix5.VictorSPX(arm_right_motor_id)
        self.shooter_state = "Disabled"
        self.shooter_motor_speeds_entry = Shuffleboard.getTab("Drivers").add(f"Shooters Motor Speed", 0.5).getEntry()

    def reset(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, 0)
        self.shooter_left_motor.set(phoenix5.ControlMode.PercentOutput, 0)
        self.shooter_right_motor.set(phoenix5.ControlMode.PercentOutput, 0)

    def get_shooter_state(self):
        return self.shooter_state
    
    def change_shooter_state(self, state):
        self.shooter_state = state

    def pick_up_note(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, self.shooter_motor_speeds)

    def stop_picking_up_note(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, 0)

    def drop_everything(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, self.shooter_motor_speeds * -1)

    def stop_dropping_everything(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, 0)

    def prime_shooter(self):
        self.shooter_left_motor.set(phoenix5.ControlMode.PercentOutput, self.shooter_motor_speeds)
        self.shooter_right_motor.set(phoenix5.ControlMode.PercentOutput, self.shooter_motor_speeds)
    
    def fire_out_note(self):
        self.intake_motor.set(phoenix5.ControlMode.PercentOutput, self.shooter_motor_speeds)

    # def move_arm_up(self):
    #     self.arm_left.set(phoenix5.ControlMode.PercentOutput, -1)
    #     self.arm_right.set(phoenix5.ControlMode.PercentOutput, 1)

    # def move_arm_down(self):
    #     self.arm_left.set(phoenix5.ControlMode.PercentOutput, 1)
    #     self.arm_right.set(phoenix5.ControlMode.PercentOutput, -1)

    # def stop_arm(self):
    #     self.arm_left.set(phoenix5.ControlMode.PercentOutput, 0)
    #     self.arm_right.set(phoenix5.ControlMode.PercentOutput, 0)
