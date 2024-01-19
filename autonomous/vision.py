import wpilib
from magicbot.state_machine import state, timed_state, AutonomousStateMachine
import ntcore
from .base_auto import BaseAuto

class Default(BaseAuto):
    MODE_NAME = "Default"
    DEFAULT = True

    def __init__(self):
        self.inst = ntcore.NetworkTableInstance.getDefault()
        self.db = self.inst.getTable("photonvision")
        self.subtbl = self.db.getSubTable("Microsoft_LiveCam_HD-3000")
        self.area = self.subtbl.getDoubleTopic("targetArea")
        self.hastarget = self.subtbl.getBooleanTopic("hasTarget")
        self.areasub = self.area.subscribe(defaultValue=0.0, options=ntcore.PubSubOptions(keepDuplicates=True, pollStorage=1))
        self.targetsub = self.hastarget.subscribe(defaultValue=False, options=ntcore.PubSubOptions(keepDuplicates=True, pollStorage=1))
    @timed_state(duration=7, first=True)
    def find_tag(self):
        targetvalue = self.targetsub.get()
        print(targetvalue)
        if targetvalue == True:
            print('found target')
            self.next_state("align")
        else:
            print("not found, relocating...")
    @timed_state(duration=5)
    def align(self):
        print('aligning...')