import phoenix6
from wpilib.shuffleboard import Shuffleboard

class Arm():
    """Class for controlling arm on robot."""

    def __init__(self, right_motor_id, left_motor_id, right_motor_bus, left_motor_bus):
        """
        Constructor for Arm.

        :param right_arm_motor_id: ID of right motor on Arm
        :type right_arm_motor_id: int
        :param left_arm_motor_id: ID of left motor on Arm
        :type left_arm_motor_id: int
        """        

        self.right_motor = phoenix6.hardware.TalonFX(right_motor_id, right_motor_bus)
        self.left_motor = phoenix6.hardware.TalonFX(left_motor_id, left_motor_bus)
       