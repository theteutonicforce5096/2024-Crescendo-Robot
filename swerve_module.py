import phoenix6
from math import fabs
from wpilib.shuffleboard import Shuffleboard

class SwerveModule():
    """Class for controlling swerve module on robot."""

    def __init__(self, module_position, turning_motor_id, driving_motor_id, cancoder_id, default_cancoder_0, 
                default_cancoder_180):
        """
        Constructor for Swerve Module

        :param module_position: Location of the module. Possible options: Front-Right, Front-Left, Back-Right, Back-Left
        :type module_position: str
        :param turning_motor_id: ID of the turning motor
        :type turning_motor_id: int
        :param driving_motor_id: ID of the driving motor
        :type driving_motor_id: int
        :param cancoder_id: ID of the CANcoder
        :type cancoder_id: int
        :param default_cancoder_0: Default value of the CANcoder at 0 degrees. Only used when Shuffleboard widget is not accessible.
        :type default_cancoder_0: float
        :param default_cancoder_180: Default value of the CANcoder at 180 degrees. Only used when Shuffleboard widget is not accessible.
        :type default_cancoder_180: float
        """

        # Hardware Initialization
        self.turning_motor = phoenix6.hardware.TalonFX(turning_motor_id)
        self.driving_motor = phoenix6.hardware.TalonFX(driving_motor_id)
        self.cancoder = phoenix6.hardware.CANcoder(cancoder_id)

        # Turning Motor Configs
        self.closed_loop_configs = phoenix6.configs.config_groups.ClosedLoopGeneralConfigs()
        self.closed_loop_configs.continuous_wrap = True
        self.turning_motor.configurator.apply(self.closed_loop_configs)
        self.feedback_configs = phoenix6.configs.config_groups.FeedbackConfigs()
        self.feedback_configs.sensor_to_mechanism_ratio = 150 / 7
        self.turning_motor.configurator.apply(self.feedback_configs)
        self.turning_motor_offset, self.module_direction = self.determine_motor_offset()

        # PID Configs
        self.slot_configs = phoenix6.configs.Slot0Configs()
        self.slot_configs.k_p = 20
        self.slot_configs.k_i = 0 
        self.slot_configs.k_d = 0
        self.turning_motor.configurator.apply(self.slot_configs) 
        self.pid = phoenix6.controls.PositionVoltage(0).with_slot(0)

        # Cancoder Configs
        self.cancoders = Shuffleboard.getTab("CANcoders")
        self.cancoder_0 = self.cancoders.add(f"{module_position} Cancoder Value for 0 Degrees", default_cancoder_0).getEntry().getFloat(default_cancoder_0) 
        self.cancoder_180 = self.cancoders.add(f"{module_position} Cancoder Value for 180 Degrees", default_cancoder_180).getEntry().getFloat(default_cancoder_180)        

    def determine_motor_offset(self):
        cancoder_offset_0 = self.cancoder.get_absolute_position().value - self.cancoder_0
        cancoder_offset_180 = self.cancoder.get_absolute_position().value - self.cancoder_180
        if fabs(cancoder_offset_0) <= fabs(cancoder_offset_180):
            turning_motor_offset = self.turning_motor.get_position().value + cancoder_offset_0
            module_direction = 1
        elif fabs(cancoder_offset_180) < fabs(cancoder_offset_0):
            turning_motor_offset = self.turning_motor.get_position().value + cancoder_offset_180
            module_direction = -1
        return turning_motor_offset, module_direction 

    def reset(self):
        """
        Sets the swerve module to face forward.
        """
        self.turning_motor.set_control(self.pid.with_position(self.turning_motor_offset)) 

    def set_velocity(self, speed, angle, direction = 1):
        """
        Sets the velocity of the swerve module.
    
        :param speed: Desired speed of the module. Must be between 0 and 1. Use wpimath.kinematics.SwerveDrive4Kinematics.desaturateWheelSpeeds 
        to reduce desired speed to be between 0 and 1. 
        :type speed: float
        :param angle: Desired angle of the module. Must already be optimized. Use wpimath.kinematics.SwerveModuleState.optimize to optimize the angle.
        :type angle: float
        :param direction: Direction of the motor. 1 is facing forward. -1 is inverted. Use the direction from wpimath.kinematics.SwerveModuleState.optimize.
        :type direction: int. 1 or -1
        """
        desired_speed = speed
        desired_position = self.turning_motor_offset + (angle / 360)
        desired_module_direction = direction * self.module_direction
            
        self.driving_motor.set_control(phoenix6.controls.DutyCycleOut(desired_speed * desired_module_direction))
        self.turning_motor.set_control(self.pid.with_position(desired_position)) 


