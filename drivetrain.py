from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics, ChassisSpeeds
from swerve_module import SwerveModule
    
class SwerveDrive:
    def __init__(self):
        FL_location = Translation2d(0.250825, 0.250825)
        FR_location = Translation2d(0.250825, -0.250825)
        BL_location = Translation2d(-0.250825, 0.250825)
        BR_location = Translation2d(-0.250825, -0.250825)

        self.kinematics = SwerveDrive4Kinematics(FL_location, FR_location, BL_location, BR_location)
        
        self.FL_module = SwerveModule("FL", 23, 13, 33, "CANivore", "CANivore", "rio", -0.002686, True)

        self.FR_module = SwerveModule("FR", 20, 10, 30, "CANivore", "CANivore", "rio", 0.003906, False)

        self.BL_module = SwerveModule("BL", 22, 12, 32, "CANivore", "CANivore", "rio", -0.476807, True)

        self.BR_module = SwerveModule("BR", 21, 11, 31, "CANivore", "CANivore", "rio", 0.002930, False)

    def reset(self):
        self.FL_module.reset()
        self.FR_module.reset()
        self.BL_module.reset()
        self.BR_module.reset()

    def stop_robot(self):
        self.FL_module.stop()
        self.FR_module.stop()
        self.BL_module.stop()
        self.BR_module.stop()

    def move_robot(self, raw_x, raw_y, rotation):
        speeds = ChassisSpeeds(raw_y, raw_x, rotation)
        FL_state, FR_state, BL_state, BR_state = self.kinematics.desaturateWheelSpeeds(self.kinematics.toSwerveModuleStates(speeds), 1)
        
        FL_state = FL_state.optimize(FL_state, self.FL_module.current_angle)
        FR_state = FR_state.optimize(FR_state, self.FR_module.current_angle)
        BL_state = BL_state.optimize(BL_state, self.BL_module.current_angle)
        BR_state = BR_state.optimize(BR_state, self.BR_module.current_angle)

        self.FL_module.move(FL_state.speed / 7.5, FL_state.angle)
        self.FR_module.move(FR_state.speed / 7.5, FR_state.angle)
        self.BL_module.move(BL_state.speed / 7.5, BL_state.angle)
        self.BR_module.move(BR_state.speed / 7.5, BR_state.angle)
