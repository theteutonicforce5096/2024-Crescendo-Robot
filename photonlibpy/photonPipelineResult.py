from dataclasses import dataclass, field

from photonlibpy.multiTargetPNPResult import MultiTargetPNPResult
from photonlibpy.packet import Packet
from photonlibpy.photonTrackedTarget import PhotonTrackedTarget


@dataclass
class PhotonPipelineResult:
    latencyMillis: float = -1.0
    timestampSec: float = -1.0
    targets: list[PhotonTrackedTarget] = field(default_factory=list)
    multiTagResult: MultiTargetPNPResult = field(default_factory=MultiTargetPNPResult)

    def populateFromPacket(self, packet: Packet) -> Packet:
        self.targets = []
        self.latencyMillis = packet.decodeDouble()
        targetCount = packet.decode8()

        self.hasWarned = False

        for _ in range(targetCount):
            target = PhotonTrackedTarget()
            target.createFromPacket(packet)
            self.targets.append(target)

        self.multiTagResult = MultiTargetPNPResult()
        self.multiTagResult.createFromPacket(packet)

        return packet

    def setTimestampSeconds(self, timestampSec: float) -> None:
        self.timestampSec = timestampSec

    def getLatencyMillis(self) -> float:
        return self.latencyMillis

    def getTimestamp(self) -> float:
        return self.timestampSec
    
    def getTargets(self) -> list[PhotonTrackedTarget]:
        return self.targets
    
    def hasTargets(self) -> bool:
        return len(self.targets) > 0
    
    def getBestTarget(self) -> PhotonTrackedTarget:
        if not self.hasTargets() and not self.hasWarned:
            errorStr = "This PhotonPipelineResult object has no targets associated with it! Please check hasTargets() \nbefore calling this method. For more information, please review the PhotonLib \ndocumentation at https://docs.photonvision.org"
            self.hasWarned = True
            raise Exception(errorStr)
        return self.targets[0] if self.hasTargets() else None
