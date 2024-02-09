import math

class PhotonUtils():
    def calculateDistanceToTargetMeters(cameraHeightMeters: float, targetHeightMeters: float, cameraPitchRadians: float, targetPitchRadians: float):
        return (targetHeightMeters - cameraHeightMeters) / math.tan(cameraPitchRadians + targetPitchRadians)