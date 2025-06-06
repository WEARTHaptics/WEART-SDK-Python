from enum import IntFlag
from dataclasses import dataclass, field
import dataclasses
from typing import List

class TrackingType(IntFlag):
	"""
	Enum for tracking types used in the application.

	Attributes:
		DEFAULT (int): The default tracking type.
		WEART_HAND (int): The tracking type related to WeArt Hand.
	"""
	DEFAULT = 0
	WEART_HAND = 1

class HandSide(IntFlag):
	"""
    Enum for hand sides (left and right).
    
    Attributes:
        Left (int): Represents the left hand.
        Right (int): Represents the right hand.
    """
	Left = 1 << 0
	Right = 1 << 1

	def __str__(self):
		"""
        Returns the string representation of the hand side in uppercase.

        Returns:
            str: The name of the hand side ('LEFT' or 'RIGHT').
        """
		return self.name.upper()
	
class HandClosingState(IntFlag):
	"""
    Enum for hand closing states.
    
    Attributes:
        Open (int): The hand is open.
        Closing (int): The hand is closing.
        Closed (int): The hand is closed.
    """
	Open = 0
	Closing = 1
	Closed = 2

class GraspingState(IntFlag):
	"""
    Enum for grasping states.
    
    Attributes:
        Grapped (int): Object is grasped.
        Released (int): Object is released.
    """
	Grapped = 0
	Released = 1

class ActuationPoint(IntFlag):
	"""
    Enum for actuation points of the hand.
    
    Attributes:
        Thumb (int): The thumb.
        Index (int): The index finger.
        Middle (int): The middle finger.
        Annular (int): The annular finger.
        Pinky (int): The pinky finger.
        Palm (int): The palm of the hand.
    """
	Thumb 	= 1 << 0
	Index 	= 1 << 1
	Middle 	= 1 << 2
	Annular = 1 << 3
	Pinky 	= 1 << 4
	Palm 	= 1 << 5

	def __str__(self):
		"""
        Returns the string representation of the actuation point.

        Returns:
            str: The name of the actuation point (e.g., 'Thumb', 'Index', etc.).
        """
		return self.name

class CalibrationStatus(IntFlag):
	"""
    Enum for the calibration status of the device.
    
    Attributes:
        IDLE (int): The calibration process has started but is not yet running.
        Calibrating (int): The calibration process is running, the user has to keep the hand still.
        Running (int): The calibration process has successfully completed.
    """
	IDLE = 0
	Calibrating = 1
	Running = 2

	def __str__(self):
		"""
        Returns the string representation of the calibration status.
        """
		return self.name

class CalibrationResult(IntFlag):
	"""
    Enum for the calibration result.

    Attributes:
        SUCCESS (int): The calibration was successful.
        FAILURE (int): The calibration failed.
    """
	SUCCESS = 0
	FAILURE = 1

	def __str__(self):
		"""
			Returns the string representation of the calibration result.
		"""
		if self == CalibrationResult.SUCCESS:
				return "SUCCESS"
		elif self == CalibrationResult.FAILURE:
			return "FAILURE"

class MiddlewareStatus(IntFlag):
	"""
    Enum for the middleware status.
    
    Attributes:
        DISCONNECTED (int): There is no device connected to the Middleware or WeArt App.
        IDLE (int): The middleware is idle.
        STARTING (int): The middleware is starting.
        RUNNING (int): The middleware is running.
        STOPPING (int): The middleware is stopping.
        UPLOADING_TEXTURES (int): The middleware is uploading textures.
        CONNECTING_DEVICE (int): The middleware is connecting to a device.
        CALIBRATION (int): The middleware is in calibration.
    """
	DISCONNECTED=0
	IDLE = 1
	STARTING = 2
	RUNNING = 3
	STOPPING = 4
	UPLOADING_TEXTURES = 5
	CONNECTING_DEVICE = 6
	CALIBRATION = 7
	
	def __str__(self):
		"""
        Returns the string representation of the middleware status.

        Returns:
            str: The name of the middleware status (e.g., 'IDLE', 'RUNNING', etc.).
        """
		return self.name

class TextureType(IntFlag):
	"""
    Enum for different texture types.
    
    Attributes:
        ClickNormal (int): Normal click texture.
        ClickSoft (int): Soft click texture.
        DoubleClick (int): Double click texture.
        AluminiumFineMeshSlow (int): Aluminium fine mesh slow texture.
        AluminiumFineMeshFast (int): Aluminium fine mesh fast texture.
        PlasticMeshSlow (int): Plastic mesh slow texture.
        ProfiledAluminiumMeshMedium (int): Profiled aluminium mesh medium texture.
        ProfiledAluminiumMeshFast (int): Profiled aluminium mesh fast texture.
        RhombAluminiumMeshMedium (int): Rhomb aluminium mesh medium texture.
        TextileMeshMedium (int): Textile mesh medium texture.
        CrushedRock (int): Crushed rock texture.
        VenetianGranite (int): Venetian granite texture.
        SilverOak (int): Silver oak texture.
        LaminatedWood (int): Laminated wood texture.
        ProfiledRubberSlow (int): Profiled rubber slow texture.
        VelcroHooks (int): Velcro hooks texture.
        VelcroLoops (int): Velcro loops texture.
        PlasticFoil2 (int): Plastic foil texture.
        Leather (int): Leather texture.
        Cotton1 (int): Cotton texture.
        Aluminium (int): Aluminium texture.
        DoubleSidedTape (int): Double sided tape texture.
    """
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
	"""
    Represents data from an accelerometer sensor.

    Attributes:
        x (float): Acceleration along the x-axis.
        y (float): Acceleration along the y-axis.
        z (float): Acceleration along the z-axis.
	"""
	x: float = 0.0
	y: float = 0.0
	z: float = 0.0

@dataclass
class GyroscopeData:
	"""
    Represents data from a gyroscope sensor.

    Attributes:
        x (float): Angular velocity along the x-axis.
        y (float): Angular velocity along the y-axis.
        z (float): Angular velocity along the z-axis.
    """
	x: float = 0.0
	y: float = 0.0
	z: float = 0.0

@dataclass
class TofData:
	"""
    Represents data from a Time-of-Flight (ToF) sensor.

    Attributes:
        distance (int): Distance measured by the ToF sensor.
    """
	distance: int = 0

@dataclass
class SensorData:
	"""
    Represents combined sensor data from an accelerometer, gyroscope, and ToF sensor.

    Attributes:
        accelerometer (AccelerometerData): The accelerometer data.
        gyroscope (GyroscopeData): The gyroscope data.
        timeOfFlight (TofData): The Time-of-Flight sensor data. This data is not available for Touch Diver Pro.
    """
	accelerometer: AccelerometerData
	gyroscope: GyroscopeData
	timeOfFlight: TofData

@dataclass
class AnalogSensorRawData:
	"""
    Represents raw data from an analog sensor.
	Analog data is not available for Touch Diver Pro.

    Attributes:
        ntcTemperatureRaw (float): Raw temperature data from the NTC sensor.
        ntcTemperatureConverted (float): Converted temperature data in Celsius.
        forceSensingRaw (float): Raw force sensing data.
        forceSensingConverted (float): Converted force sensing data.
    """
	ntcTemperatureRaw: float
	ntcTemperatureConverted: float
	forceSensingRaw: float
	forceSensingConverted: float

@dataclass
class MiddlewareConnectedDevice:
	"""
    Represents a connected device in the middleware.

    Attributes:
        macAddress (str): The MAC address of the connected device.
        handSide (HandSide): The hand side of the connected device (left or right).
    """
	macAddress: str
	handSide: HandSide

@dataclass
class MiddlewareStatusData:
	"""
    Represents the status of the Middleware.

    Attributes:
        status (MiddlewareStatus): The current status of the Middleware.
        version (str): The version of the Middleware.
        statusCode (int): A code representing the status of the Middleware.
        errorDesc (str): A description of any error in the Middleware.
        actuationsEnabled (bool): Whether actuations are enabled in the Middleware.
        connectedDevices (List[MiddlewareConnectedDevice]): The list of connected devices.
        timestamp (int): The timestamp of the status data.
    """
	status: MiddlewareStatus
	version: str
	statusCode: int
	errorDesc: str
	actuationsEnabled: bool
	connectedDevices: List[MiddlewareConnectedDevice]
	timestamp: int = 0

@dataclass
class WeArtAppStatusData:
	"""
    Represents the status of the WeArt App.

    Attributes:
        status (MiddlewareStatus): The current status of the WeArt App.
        version (str): The version of the WeArt App.
        statusCode (int): A code representing the status of the WeArt App.
        errorDesc (str): A description of any error in the WeArt App.
		warningCode (int): The warning code representing WeArtApp warning state.
        warningDesc (str): A description of any warning that occurred.
        actuationsEnabled (bool): Whether actuations are enabled in the WeArt App.
        connectionType (str): The type of connection (e.g., 'BLE').
        autoconnection (bool): Whether auto-connection is enabled.
        trackingPlayback (bool): Whether tracking playback is enabled.
        rawDataLog (bool): Whether raw data logging is enabled.
        sensorOnMask (bool): Whether the sensor is turned on.
        connectedDevices (List[MiddlewareConnectedDevice]): The list of connected devices.
        timestamp (int): The timestamp of the status data.
    """
	status: MiddlewareStatus
	version: str
	statusCode: int
	errorDesc: str
	warningCode: int
	warningDesc: str
	actuationsEnabled: bool
	connectionType: str
	autoconnection: bool
	trackingPlayback: bool                              
	rawDataLog: bool
	sensorOnMask: bool
	connectedDevices: List[MiddlewareConnectedDevice] = field(default_factory=list)
	timestamp: int = 0

@dataclass
class ThimbleStatus:
	"""
    Represents the status of a thimble on the device.

    Attributes:
        id (ActuationPoint): The actuation point ID of the thimble (e.g., Palm, Thumb, etc.).
        connected (bool): Whether the thimble is connected.
        statusCode (int): A code representing the thimble's status.
        errorDesc (str): A description of any error related to the thimble.
    """
	id: ActuationPoint = ActuationPoint.Palm
	connected: bool = False
	statusCode: int = 0
	errorDesc: str = ""

@dataclass
class ConnectedDeviceStatus:
	"""
    Represents the status of a connected device.

    Attributes:
        macAddress (str): The MAC address of the connected device.
        handSide (HandSide): The hand side of the device (left or right).
        batteryLevel (int): The battery level of the device in percentage (0%-100%).
        charging (bool): Whether the device is currently charging.
        thimbles (List[ThimbleStatus]): The list of thimbles connected to the device.
    """
	macAddress: str = ""
	handSide: HandSide = HandSide.Left
	batteryLevel: int = 0
	charging: bool = False
	thimbles: List[ThimbleStatus] = field(default_factory=lambda: [ThimbleStatus()]) #std::vector<ThimbleStatus> thimbles;

@dataclass
class G2ConnectionStatus:
	"""
    Represents the connection status of the Touch Diver Pro device.

    Attributes:
        bluetoothOn (bool): Whether Bluetooth is turned on.
        bluetoothConnected (bool): Whether Bluetooth is connected.
        wifiOn (bool): Whether Wi-Fi is turned on.
        wifiConnected (bool): Whether Wi-Fi is connected.
        usbConnected (bool): Whether the USB is connected.
    """
	bluetoothOn: bool
	bluetoothConnected: bool
	wifiOn: bool
	wifiConnected: bool
	usbConnected: bool

@dataclass 
class G2MasterStatus:
	"""
    Represents the master status of the Touch Diver Pro device.

    Attributes:
        batteryLevel (int): The battery level of the Touch Diver Pro master device.
        charging (bool): Whether the Touch Diver Pro master device is charging.
        chargeCompleted (bool): Whether the charge is completed.
        connection (G2ConnectionStatus): The connection status of the Touch Diver Pro device.
        imuFault (bool): Whether there is a fault with the master IMU.
        adcFault (bool): Whether there is a fault with the master ADC.
        buttonPushed (bool): Whether the button was pushed.
    """
	batteryLevel: int
	charging: bool
	chargeCompleted: bool
	connection: G2ConnectionStatus
	imuFault: bool
	adcFault: bool
	buttonPushed: bool

@dataclass
class G2NodeStatus:
	"""
    Represents the status of a node in the Touch Diver Pro device.

    Attributes:
        id (ActuationPoint): The actuation point of the node.
        connected (bool): Whether the node is connected.
        imuFault (bool): Whether there is a fault with the IMU on the node.
        adcFault (bool): Whether there is a fault with the ADC on the node. This field now represents fault on Magnetometer.
        tofFault (bool): Whether there is a fault with the ToF sensor on the node. Since there is no ToF sensor installed in Touch Diver Pro, this is always True.
    """
	id: ActuationPoint = ActuationPoint.Thumb
	connected: bool = False
	imuFault: bool = False
	adcFault: bool = False
	tofFault: bool = False

@dataclass
class G2DeviceStatus:
	"""
    Represents the status of a Touh Diver Pro device.

    Attributes:
        macAddress (str): The MAC address of the Touh Diver Pro device.
        handSide (HandSide): The hand side of the device (left or right).
        signalStrength (float): The signal strength of the device (in dBm).
        master (G2MasterStatus): The master status of the Touh Diver Pro device.
        nodes (List[G2NodeStatus]): The list of nodes in the Touh Diver Pro device.
    """
	macAddress: str
	handSide: HandSide
	signalStrength: float
	master: G2MasterStatus
	nodes: List[G2NodeStatus] = field(default_factory=lambda: [G2NodeStatus()])

@dataclass
class TDProStatusData:
	"""
    Represents a list of Touch Diver Pro devices status.

    Attributes:
        devices (List[G2DeviceStatus]): The list of Touch Diver Pro devices status.
    """
	devices: List[G2DeviceStatus] = field(default_factory=lambda: [G2DeviceStatus()])

def dataclass_from_list(klass, l):
	"""
    Converts a list of dictionaries into a list of dataclass instances of the specified class.

    Args:
        klass (type): The class type to convert the dictionaries into.
        l (list): A list of dictionaries where each dictionary contains data for a dataclass.

    Returns:
        list: A list of dataclass instances created from the dictionaries.
    """
	ret = []
	for elem in l:
		ret.append(dataclass_from_dict(klass, elem))
	return ret

def dataclass_from_dict(klass, d):
	"""
    Converts a dictionary into a dataclass instance of the specified class.

    Args:
        klass (type): The class type to convert the dictionary into.
        d (dict): A dictionary containing data to populate the dataclass fields.

    Returns:
        object: An instance of the specified class populated with data from the dictionary.
    """
	# If type of class is a dataclass, proceed with deserialization
	if dataclasses.is_dataclass(klass):
		# Get the field types for the dataclass
		fieldtypes = {f.name: f.type for f in dataclasses.fields(klass)}
		data = {}
        
		for f in fieldtypes:
			# If the field exists in the dictionary, proceed with deserialization
			if f in d:
				if isinstance(d[f], list):
					# If the field is a list, recursively deserialize its elements
					data[f] = dataclass_from_list(fieldtypes[f].__args__[0], d[f])
				else:
					# Recursively deserialize fields that are not "special" types
					data[f] = dataclass_from_dict(fieldtypes[f], d[f])
			else:
				# If the field does not exist in the dictionary, assign a default value
				if klass == MiddlewareStatus:
					if f == 'connectionType':
						data[f] = 'BLE'
					elif f == 'autoconnection':
						data[f] = False
					elif f == 'trackingPlayback':
						data[f] = False
					elif f == 'rawDataLog':
						data[f] = False
					elif f == 'sensorOnMask':
						data[f] = False
					else:
						data[f] = None
				else:
					data[f] = None

		# Create the dataclass instance with the deserialized data
		k = klass(**data)
		return k
	else:
		# If the type of class is a dataclass, proceed with deserialization
		if klass == MiddlewareStatus:
			return MiddlewareStatus[d]
		if klass == ActuationPoint:
			return ActuationPoint[str(d).capitalize()]
		if klass == HandSide:
			return HandSide[str(d).capitalize()]
		if klass == List[ThimbleStatus]:
			return dataclass_from_list(ThimbleStatus, d)
		
		# If the type of class is not a dataclass, return the dictionary
		return d

def dict_from_dataclass(k):
	"""
    Converts a dataclass instance into a dictionary, recursively handling nested dataclasses.

    Args:
        k (object): The dataclass instance to convert into a dictionary.

    Returns:
        dict: A dictionary representation of the dataclass instance.
    """
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

WEART_SDK_VERSION = "2.0.0"
WEART_SDK_TYPE = "SdkLLPY"

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
