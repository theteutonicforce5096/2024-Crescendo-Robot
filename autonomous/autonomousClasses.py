from autonomous.base_auto import BaseAuto
from magicbot.state_machine import state, timed_state, AutonomousStateMachine
from subsystems.drivetrain import SwerveDrive


class Move(BaseAuto):
    MODE_NAME = "Move Out Of Box"
    DEFAULT = True

    drivetrain = SwerveDrive()

    @timed_state(duration=2, first=True)
    def moooooove(self):
        self.drivetrain.move_robot(0.1, 0, 0)