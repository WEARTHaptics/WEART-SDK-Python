from enum import Enum

class TrackingType(Enum):
    DEFAULT = 0
    WEART_HAND = 1

class HandSide(Enum):
	#HSnone = 0	
	Left = 1 << 0,
	Right = 1 << 1,


class ActuationPoint(Enum):
	#APnone	= 0
	Thumb = 1 << 0,
	Index = 1 << 1,
	Middle = 1 << 2,
	Palm = 1 << 3,



DEFAULT_IP_ADDRESS = "127.0.0.1"
DEFAULT_TCP_PORT = 13031

WEART_SDK_VERSION = "1.0.0"
WEART_SDK_TYPE = "SdkLLCPP"

defaultTemperature = 0.5
minTemperature = 0.0
maxTemperature = 1.0

defaultForce = 0.0
minForce = 0.0
maxForce = 1.0

defaultClosure = 0.0
minClosure = 0.0
maxClosure = 1.0

defaultAbduction = 0.442

defaultTextureIndex = 0
minTextureIndex = 0
maxTextureIndex = 21
nullTextureIndex = 255

defaultCollisionMultiplier = 20.0
minCollisionMultiplier = 0.0
maxCollisionMultiplier = 100.0

defaultVolumeTexture = 100.0
minVolumeTexture = 0.0
maxVolumeTexture = 100.0

thresholdThumbClosure = 0.5
thresholdIndexClosure = 0.5
thresholdMiddleClosure = 0.5

defaultGraspForce = 0.3
dynamicForceSensibility = 10.0
