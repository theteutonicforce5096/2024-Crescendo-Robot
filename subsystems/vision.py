import wpilib
from magicbot.state_machine import state, timed_state, AutonomousStateMachine
import ntcore
import phoenix6
from autonomous.base_auto import BaseAuto
import cv2

class Vision(BaseAuto):
    MODE_NAME = "Default"
    DEFAULT = True

    def __init__(self):
        self.inst = ntcore.NetworkTableInstance.getDefault()
        self.db = self.inst.getTable("photonvision")
        self.subtbl = self.db.getSubTable("Microsoft_LiveCam_HD-3000")
        self.area = self.subtbl.getDoubleTopic("targetArea").subscribe(defaultValue=False, options=ntcore.PubSubOptions(keepDuplicates=True, pollStorage=1))
        self.hastarget = self.subtbl.getBooleanTopic("hasTarget").subscribe(defaultValue=False, options=ntcore.PubSubOptions(keepDuplicates=True, pollStorage=1))
        self.yaw = self.subtbl.getDoubleTopic("targetYaw").subscribe(defaultValue=False, options=ntcore.PubSubOptions(keepDuplicates=True, pollStorage=1))
    @timed_state(duration=7, first=True)
    def find_tag(self):
        targetvalue = self.hastarget.get()
        print(targetvalue)
        if targetvalue == True:
            print('found target')
            self.next_state("align")
        else:
            print("not found, relocating...")
    @timed_state(duration=5)
    def align(self):
        print('aligning...')
        currentyaw = self.yaw.get()
        currentbearing = 0.00
        currentrange = 10
        if currentbearing > 0:
            # turn left
            pass
        elif currentbearing < 0:
            # turn right
            pass
        else:
            if currentyaw > 0:
                # strafe right
                pass
            elif currentyaw < 0:
                # strafe left
                pass
            else:
                desiredrange = 0
                #we need to figure out range values. but we assume 0 is going to be right in front of the apriltag
                if currentrange > desiredrange:
                    # move forward
                    pass
                elif currentrange < desiredrange:
                    # move backward
                    pass
                else:
                    self.next_state("finish")
                    pass
    @timed_state(duration=2)
    def finish(self):
        pass


        
