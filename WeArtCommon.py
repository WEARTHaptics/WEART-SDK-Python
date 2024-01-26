from enum import IntFlag

class TrackingType(IntFlag):
    DEFAULT = 0
    WEART_HAND = 1

class HandSide(IntFlag):
	#HSnone = 0	
	Left = 1 << 0
	Right = 1 << 1

class ActuationPoint(IntFlag):
	#APnone	= 0
	Thumb = 1 << 0
	Index = 1 << 1
	Middle = 1 << 2
	Palm = 1 << 3

class CalibrationStatus(IntFlag):
	IDLE = 0
	Calibrating = 1
	Running = 2


class TextureType(IntFlag):
	ClickNormal = 0
	ClickSoft = 1
	DoubleClick = 2
	AluminiumFineMeshSlow = 3
	AluminiumFineMeshFast = 4
	PlasticMeshSlow = 5
	ProfiledAluminiumMeshMedium = 6
	ProfiledAluminiumMeshFast = 7
	RhombAluminiumMeshMedium = 8
	TextileMeshMedium = 9
	CrushedRock = 10
	VenetianGranite = 11
	SilverOak = 12
	LaminatedWood = 13
	ProfiledRubberSlow = 14
	VelcroHooks = 15
	VelcroLoops = 16
	PlasticFoil2 = 17
	Leather = 18
	Cotton1 = 19
	Aluminium = 20
	DoubleSidedTape = 21



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
