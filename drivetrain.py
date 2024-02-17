from wpimath.geometry import Translation2d, Rotation2d
from wpimath.kinematics import SwerveDrive4Kinematics, ChassisSpeeds
from swerve_module import SwerveModule
import navx
    
class SwerveDrive:
    def __init__(self):
        front_left_location = Translation2d(0.250825, 0.250825)
        front_right_location = Translation2d(0.250825, -0.250825)
        back_left_location = Translation2d(-0.250825, 0.250825)
        back_right_location = Translation2d(-0.250825, -0.250825)

        self.kinematics = SwerveDrive4Kinematics(front_left_location, front_right_location, back_left_location, back_right_location)
        self.front_left_module = SwerveModule("FL", 23, 13, 33, "CANivore", "CANivore", "rio", -0.002686, True)
        self.front_right_module = SwerveModule("FR", 20, 10, 30, "CANivore", "CANivore", "rio", 0.003906, False)
        self.back_left_module = SwerveModule("BL", 22, 12, 32, "CANivore", "CANivore", "rio", -0.476807, True)
        self.back_right_module = SwerveModule("BR", 21, 11, 31, "CANivore", "CANivore", "rio", 0.002930, False)

        self.gyro = navx.AHRS.create_spi()

    def reset(self):
        self.front_left_module.reset()
        self.front_right_module.reset()
        self.back_left_module.reset()
        self.back_right_module.reset()
        self.gyro.reset()

    def get_current_robot_angle(self):
        current_robot_angle = self.gyro.getAngle() * -1
        if current_robot_angle > 180: 
            current_robot_angle -= 360
        elif current_robot_angle < -180:
            current_robot_angle += 360

        return current_robot_angle

    def move_robot(self, raw_x, raw_y, rotation):
        current_robot_angle = self.get_current_robot_angle()
        speeds = ChassisSpeeds.fromFieldRelativeSpeeds(raw_y, raw_x, rotation, Rotation2d.fromDegrees(current_robot_angle))
        FL_state, FR_state, BL_state, BR_state = self.kinematics.desaturateWheelSpeeds(self.kinematics.toSwerveModuleStates(speeds), 1)
        
        FL_state = FL_state.optimize(FL_state, self.front_left_module.current_angle)
        FR_state = FR_state.optimize(FR_state, self.front_right_module.current_angle)
        BL_state = BL_state.optimize(BL_state, self.back_left_module.current_angle)
        BR_state = BR_state.optimize(BR_state, self.back_right_module.current_angle)

        self.front_left_module.move(FL_state.speed / 7.5, FL_state.angle)
        self.front_right_module.move(FR_state.speed / 7.5, FR_state.angle)
        self.back_left_module.move(BL_state.speed / 7.5, BL_state.angle)
        self.back_right_module.move(BR_state.speed / 7.5, BR_state.angle)

    def stop_robot(self):
        self.front_left_module.stop()
        self.front_right_module.stop()
        self.back_left_module.stop()
        self.back_right_module.stop()
