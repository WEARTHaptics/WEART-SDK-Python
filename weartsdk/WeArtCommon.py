from enum import IntFlag
from dataclasses import dataclass, field
import dataclasses
from typing import List
import logging
import json

class TrackingType(IntFlag):
    DEFAULT = 0
    WEART_HAND = 1

class HandSide(IntFlag):
	#HSnone = 0	
	Left = 1 << 0
	Right = 1 << 1
	

class HandClosingState(IntFlag):
	Open = 0
	Closing = 1
	Closed = 2

class GraspingState(IntFlag):
	Grapped = 0
	Released = 1

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

class MiddlewareStatus(IntFlag):
	DISCONNECTED=0
	IDLE = 1
	STARTING = 2
	RUNNING = 3
	STOPPING = 4
	UPLOADING_TEXTURES = 5
	CONNECTING_DEVICE = 6
	CALIBRATION = 7
	def __str__(self):
		return self.name

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

@dataclass
class AccelerometerData:
	x: float = 0.0
	y: float = 0.0
	z: float = 0.0


@dataclass
class GyroscopeData:
	x: float = 0.0
	y: float = 0.0
	z: float = 0.0

@dataclass
class TofData:
	distance: int = 0

@dataclass
class SensorData:
	accelerometer: AccelerometerData
	gyroscope: GyroscopeData
	timeOfFlight: TofData

@dataclass
class AnalogSensorRawData:
	ntcTemperatureRaw:float
	ntcTemperatureConverted:float
	forceSensingRaw:float
	forceSensingConverted:float

@dataclass
class MiddlewareConnectedDevice:
	macAddress:str
	handSide:HandSide

@dataclass
class MiddlewareStatusData:
	status:MiddlewareStatus
	version:str
	statusCode:int
	errorDesc:str
	actuationsEnabled:bool
	connectedDevices:list #std::vector<MiddlewareConnectedDevice>
	timestamp:int = 0

@dataclass
class ThimbleStatus:
	id:ActuationPoint = ActuationPoint.Palm
	connected:bool = False
	statusCode:int = 0
	errorDesc:str = ""

@dataclass
class ConnectedDeviceStatus:
	macAddress:str = ""
	handSide: HandSide = HandSide.Left
	batteryLevel: int = 0
	charging: bool = False
	thimbles: List[ThimbleStatus] = field(default_factory=lambda: [ThimbleStatus()]) #std::vector<ThimbleStatus> thimbles;


def dataclass_from_list(klass, l):
	ret = []
	for elem in l:
		ret.append(dataclass_from_dict(klass, elem))
	return ret

def dataclass_from_dict(klass, d):
	if dataclasses.is_dataclass(klass):
		fieldtypes = {f.name:f.type for f in dataclasses.fields(klass)}
		k = klass(**{f:dataclass_from_dict(fieldtypes[f],d[f]) for f in d})
		return k
	else:
		if klass == MiddlewareStatus:
			return MiddlewareStatus[d]
		if klass == ActuationPoint:
			return ActuationPoint[str(d).capitalize()]
		if klass == HandSide:
			return HandSide[str(d).capitalize()]
		if klass == List[ThimbleStatus]:
			return dataclass_from_list(ThimbleStatus, d)
		return d # Not a dataclass field

def dict_from_dataclass(k):
	#to be checked, IntFlags are not well represented
	if dataclasses.is_dataclass(k):
		return  dataclasses.asdict(k)
	elif isinstance(k, list):
		l = []
		for elem in k:
			l.append(dict_from_dataclass(elem))
		return l



DEFAULT_IP_ADDRESS = "127.0.0.1"
DEFAULT_TCP_PORT = 13031

WEART_SDK_VERSION = "1.0.3"
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

__all__ = [] # so we do not fill up the imports
