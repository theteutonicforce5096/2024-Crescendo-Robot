from wpimath.geometry import Translation2d, Rotation2d
from wpimath.kinematics import SwerveDrive4Kinematics, ChassisSpeeds
from swerve_module import SwerveModule
    
class SwerveDrive:
    def __init__(self):
        FL_location = Translation2d(0.3175, 0.3175)
        FR_location = Translation2d(0.3175, -0.3175)
        BL_location = Translation2d(-0.3175, 0.3175)
        BR_location = Translation2d(-0.3175, -0.3175)

        self.kinematics = SwerveDrive4Kinematics(FL_location, FR_location, BL_location, BR_location)
        
        self.FL_module = SwerveModule("FL", 23, 13, 33, -0.002686, -1)

        self.FR_module = SwerveModule("FR", 20, 10, 30, 0.003906, 1)

        self.BL_module = SwerveModule("BL", 22, 12, 32, -0.476807, -1)

        self.BR_module = SwerveModule("BR", 21, 11, 31, 0.002930, 1)

    def reset(self):
        self.FL_module.reset()
        self.FR_module.reset()
        self.BL_module.reset()
        self.BR_module.reset()
    
    # def optimize_angle(self, current_angle, desired_angle):
    #     desired_angle = (desired_angle + 360) % 360
    #     print(f"Desired: {desired_angle}")
    #     print(f"Current: {current_angle}")
    #     if desired_angle - current_angle == 180:
    #         module_direction = -1
    #     elif desired_angle + current_angle == -180:
    #         module_direction = 1
    #     elif desired_angle - current_angle > 90:
    #         desired_angle -= 180
    #         module_direction = -1
    #     elif desired_angle + current_angle < -90:
    #         desired_angle += 180
    #         module_direction = 1
    #     else:
    #         module_direction = 1

    #     return desired_angle, module_direction

    def move_robot(self, raw_x, raw_y, rotation):
        speeds = ChassisSpeeds(raw_y, raw_x, rotation)
        FL_state, FR_state, BL_state, BR_state = self.kinematics.desaturateWheelSpeeds(self.kinematics.toSwerveModuleStates(speeds), 1)
        
        FL_state = FL_state.optimize(FL_state, self.FL_module.current_angle)
        FR_state = FR_state.optimize(FR_state, self.FR_module.current_angle)
        BL_state = BL_state.optimize(BL_state, self.BL_module.current_angle)
        BR_state = BR_state.optimize(BR_state, self.BR_module.current_angle)
        
        #FL_angle, FL_direction = self.optimize_angle(self.FL_module.current_angle, FL_state.angle.degrees() * -1)
        #FR_angle, FR_direction = self.optimize_angle(self.FR_module.current_angle, FR_state.angle.degrees() * -1)
        #BL_angle, BL_direction = self.optimize_angle(self.BL_module.current_angle, BL_state.angle.degrees() * -1)
        #BR_angle, BR_direction = self.optimize_angle(self.BR_module.current_angle, BR_state.angle.degrees() * -1)

        self.FL_module.set_velocity(FL_state.speed / 10, FL_state.angle)
        self.FR_module.set_velocity(FR_state.speed / 10, FR_state.angle)
        self.BL_module.set_velocity(BL_state.speed / 10, BL_state.angle)
        self.BR_module.set_velocity(BR_state.speed / 10, BR_state.angle)

    def stop_robot(self):
        self.FL_module.stop()
        self.FR_module.stop()
        self.BL_module.stop()
        self.BR_module.stop()
