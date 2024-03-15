from math import sin

class PhotonUtils():
    def calculateDistanceToTargetMeters(cameraHeightMeters: float, targetHeightMeters: float, cameraPitchRadians: float, targetPitchRadians: float):
        """
        :param cameraHeightMeters: The physical height of the camera off the floor in meters.
        :param targetHeightMeters: The physical height of the target off the floor in meters. This 
        should be the height of whatever is being targeted (i.e. if the targeting region is set to
        top, this should be the height of the top of the target).
        :param cameraPitchRadians: The pitch of the camera from the horizontal plane in radians. Positive values up.
        :param targetPitchRadians: The pitch of the target in the camera's lens in radians. Positive values up.
        """
        return (targetHeightMeters - cameraHeightMeters) / sin(cameraPitchRadians + targetPitchRadians)