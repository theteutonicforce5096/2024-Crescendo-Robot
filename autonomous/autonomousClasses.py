from autonomous.base_auto import BaseAuto
from magicbot.state_machine import state, timed_state, AutonomousStateMachine
from subsystems.drivetrain import SwerveDrive
from subsystems.shooter import Shooter


class Move(BaseAuto):
    MODE_NAME = "Move Out Of Box"
    DEFAULT = True

    drivetrain = SwerveDrive()

    @timed_state(duration=2, first=True)
    def moooooove(self):
        self.drivetrain.move_robot(0.1, 0, 0)

class ShootNScoot(BaseAuto):
    MODE_NAME = "Shoot N Scoot"
    Default = False

    drivetrain = SwerveDrive()
    shooter = Shooter(40, 41, 42, False, False, False, 0.7)

    @timed_state(duration=2, first=True, next_state="scoot")
    def shoot(self):
        self.shooter.release_note()

    @timed_state(duration=2)
    def scoot(self):
        self.drivetrain.move_robot(0.1, 0, 0)