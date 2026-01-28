# Weart Low-Level Python SDK

The Weart Low-Level Python SDK allows you to connect to the WEART-Middleware or WEART-App (desktop applications) and perform various actions with the TouchDIVER devices:
* Start and Stop the middleware operations
* Calibrate the device
* Receive tracking data from the devices
* Receive raw data from the thimble's motion sensors 
* Receive analog raw data from the thimble's sensors (not available for TouchDIVER PRO)
* Send haptic effects to the devices

## Documentation, SDKs and other resources
WEART Download page [here](https://weart.it/developer-guide/)

# Setup
The minimum setup to use the weart SDK consists of:
* A PC with the Middleware or WEART-App installed
* A TouchDIVER device
* A Python project using the Low-Level SDK 

## pip
This repository can be fetched using
```sh
pip install weartsdk
```

## Local
You can clone the SDK repository. Copy the `weartsdk` directory in your project.
Import any class and reference on your project.

# Usage
You can access most objects through the wildcard import:
```py
from weartsdk import *
```

Otherwise, here are the most common imports:
```py
from weartsdk.WeArtHapticObject import WeArtHapticObject
from weartsdk.WeArtCommon import HandSide, ActuationPoint, CalibrationStatus, TextureType
from weartsdk.WeArtTemperature import WeArtTemperature
from weartsdk.WeArtTexture import WeArtTexture
from weartsdk.WeArtForce import WeArtForce
from weartsdk.WeArtEffect import TouchEffect
from weartsdk.WeArtTrackingCalibration import WeArtTrackingCalibration
from weartsdk.WeArtThimbleTrackingObject import WeArtThimbleTrackingObject
from weartsdk.WeArtTrackingRawData import WeArtTrackingRawData
from weartsdk.MiddlewareStatusListener import MiddlewareStatusListener
from weartsdk.WeArtAnalogSensorData import WeArtAnalogSensorData

from weartsdk.WeArtClient import WeArtClient
from weartsdk import WeArtCommon
```

# Example scripts
In the repository, you will find an examples/ directory with various examples demonstrating how to use all the snippets you need to work with the WEART SDK.

# Objects
## WeArtClient
This object represents the connection to the Middleware or WEART-App.
In order to operate with TouchDIVER devices, it's necessary to:
1. Create a WeArtClient object
```py
	client = WeArtClient(WeArtCommon.DEFAULT_IP_ADDRESS, WeArtCommon.DEFAULT_TCP_PORT)
```
2. Connect to the Middleware or WEART-App
```py
client.Run()
```
3. Start the device(s)
```py
client.Start()
```

The client object has the following methods:
- `def Run()`: Establishes a socket connection with the Middleware or WeArtApp.
- `def IsConnected() -> bool`: Returns `True` if the socket connection is established, `False` otherwise.
- `def Close()`: Closes the socket connection.
- `def Start()`: Starts the connected device(s).
- `def Stop()`: Stops the connected device(s).
- `def StartCalibration()`: Starts the calibration process.
- `def StopCalibration()`: Stops the calibration process.
- `def StartRawData()`: Starts raw data collection from the device(s).
- `def StopRawData()`: Stops raw data collection from the device(s).
- `def AddThimbleTracking(trackingObject: WeArtThimbleTrackingObject)`: Adds a thimble tracking object to the client.
- `def RemoveThimbleTracking(trackingObject: WeArtThimbleTrackingObject)`: Removes a thimble tracking object from the client.
- `def ThimbleTrackingObjectsSize() -> int`: Returns the number of tracked thimble objects.
- `def AddMessageListener(listener: WeArtMessageListener)`: Adds a message listener to handle incoming messages.
- `def RemoveMessageListener(listener: WeArtMessageListener)`: Removes a message listener.
- `def AddConnectionStatusCallback(callback)`: Adds a callback for connection status changes.
- `def AddErrorCallback(callback)`: Adds a callback for error notifications.


## MiddlewareStatusListener
This object represents the status of the Middleware or WEART-App.
Middleware status includes the following information:
* **timestamp**: the timestamp of the last received status update message  
* **status**: the status of the Middleware or WEART-App  
* **version**: the version of the Middleware or WEART-App  
* **status code**: the status code of the Middleware or WEART-App (listed below)
* **error description**: the error description of the Middleware or WEART-App  
* **actuation enabled**: whether the actuation is enabled or not  
* **connected devices**: the list of connected devices  

The following fields are available only for TouchDIVER PRO:
* **warning code**: the warning code of the WEART-App (listed below)
* **warning description**: the warning description of the WEART-App
* **connection type**: how the WEART-App is connected to the device(s)  
* **autoconnection**: whether autoconnection is enabled or not  
* **tracking playback**: whether the tracking playback is enabled or not  
* **raw data log**: whether the raw data log is enabled or not  
* **sensor on mask**: indicates if sensors are enabled  

### Example Object

An example of a `MiddlewareStatusUpdate` object:

- `timestamp`: `int` → `1712136792`  
- `status`: `MiddlewareStatus` → `IDLE`  
- `version`: `str` → `"1.2.3"`  
- `statusCode`: `int` → `200`  
- `errorDesc`: `str` → `""`  
- `actuationsEnabled`: `bool` → `True`  
- `connectedDevices`: `List[MiddlewareConnectedDevice]` →  
  - `MiddlewareConnectedDevice(macAddress="00:1A:7D:DA:71:13", handSide=HandSide.LEFT)`  
  - `MiddlewareConnectedDevice(macAddress="00:1A:7D:DA:71:14", handSide=HandSide.RIGHT)`
- `warningCode`: `int` → `0`  *(TouchDIVER PRO only)*
- `warningDesc`: `str` → `""`  *(TouchDIVER PRO only)*
- `connectionType`: `str` → `"USB"`  *(TouchDIVER PRO only)*  
- `autoconnection`: `bool` → `True`  *(TouchDIVER PRO only)*  
- `trackingPlayback`: `bool` → `False`  *(TouchDIVER PRO only)*  
- `rawDataLog`: `bool` → `True`  *(TouchDIVER PRO only)*  
- `sensorOnMask`: `bool` → `False`  *(TouchDIVER PRO only)*  

### Status Codes
The status codes (along with their description) are:

| Status Code |   | Description |
|---|---|---|
| 0 | OK | Ok |
| 100 | START_GENERIC_ERROR | Can't start generic error: Stopping |
| 101 | CONNECT_THIMBLE | Unable to start, connect at least one thimble and retry |
| 102 | WRONG_THIMBLES | Unable to start, connect the right thimbles matched to the bracelet and retry |
| 103 | BATTERY_TOO_LOW | Battery is too low, cannot start |
| 104 | FIRMWARE_COMPATIBILITY | Can't start while the devices are connected to the power supply |
| 105 | SET_IMU_SAMPLE_RATE_ERROR | Error while setting IMU Sample Rate! Device Disconnected! |
| 106 | RUNNING_SENSOR_ON_MASK | Inconsistency on Analog Sensors raw data! Please try again or Restart your device/s! |
| 107 | RUNNING_DEVICE_CHARGING | Can't start while the devices are connected to the power supply |
| 200 | CONSECUTIVE_TRACKING_ERRORS | Too many consecutive running sensor errors, stopping session |
| 201 | DONGLE_DISCONNECT_RUNNING | BLE Dongle disconnected while running, stopping session |
| 202 | TD_DISCONNECT_RUNNING | TouchDIVER disconnected while running, stopping session |
| 203 | DONGLE_CONNECTION_ERROR | Error on Dongle during connection phase! |
| 204 | USB_CONNECTION_ERROR | Can not use the device through Bluetooth while connected to a USB port |
| 205 | BLE_BAD_SIGNAL_ERROR | Bad Bluetooth signal |
| 300 | STOP_GENERIC_ERROR | Generic error occurred while stopping session |

**⚠️ Important:** The description of each status code might change between different Middleware versions, use the status code to check instead of the description.

### Warning Codes
The warning codes (along with their description) are:

| Warning Code |   | Description |
|---|---|---|
| 0 | OK | Ok |
| 100 | GENERIC_WARNING | Check WeArtApp |
| 101 | BATTERY_LOW | Device battery is low |
| 102 | SIGNAL_WEAK | Connection signal is weak |

You can get Middleware or WEART-App status by asking it anytime or using appropriate callbacks that are called when the status changes.

### Usage example

#### Asking for the status anytime
```py
# Create a listener to receive status from Middleware
mwListener = MiddlewareStatusListener()
# Add the listener to the client
client.AddMessageListener(mwListener)

# Ask for the status
mwStatus = client.LastStatus()

print("Last status updated at: " + str(mwStatus.timestamp))
print("Middleware status is: " + str(mwStatus.status))
print("Middleware version is: " + str(status.version))
```

#### Using callbacks
```py
# Create an appropriare callback
def statusUpdateCallback(status):
	print("Middleware status updated at: " + str(status.timestamp))
	print("Middleware status is: " + str(status.status))
	if len(status.connectedDevices) > 0:
		print("There are " + str(len(status.connectedDevices)) + " connected devices")

# Create a listener to receive status from Middleware
mwListener = MiddlewareStatusListener()
# Add the callback to the listener
mwListener.AddStatusCallback(statusUpdateCallback)
# Add the listener to the client
client.AddMessageListener(mwListener)
```

## DeviceStatusListener
This object represents the status of the TouchDIVER device(s).\
**⚠️ Important:** This object is not compatible with TouchDIVER PRO, use the TDProStatusListener instead.\
Device status includes the following information:
* **timestamp**: the timestamp of the last received status update message
* **devices**: the list of connected devices' status

Each device status includes the following information:
* **mac address**: the MAC address of the device
* **handSide**: the side of the device
* **battery level**: the battery level of the device
* **charging**: whether the device is charging or not
* **thimbles**: the list of thimbles' status

Each thimble status includes the following information:
* **ID**: the ID of the thimble (e.g. "Thumb", "Annular", ect.)
* **connected**: whether the thimble is connected or not
* **status code**: the status code of the thimble
* **error description**: the error description of the thimble

### Example Object

#### An example of a `DeviceStatusUpdate` object:

- `timestamp`: `int` → `1712136792`  
- `devices`: `List[ConnectedDeviceStatus]` →  
  - `ConnectedDeviceStatus(macAddress="00:1A:7D:DA:71:13", handSide=HandSide.LEFT, batteryLevel=85, charging=False, thimbles=[ThimbleStatus(id=ActuationPoint.Thumb, connected=True, statusCode=0, errorDesc="")])` 

#### `ConnectedDeviceStatus` fields:
- `macAddress`: `str` → `"00:1A:7D:DA:71:13"`  
- `handSide`: `HandSide` → `HandSide.LEFT`  
- `batteryLevel`: `int` → `85`  
- `charging`: `bool` → `False`  
- `thimbles`: `List[ThimbleStatus]` →  
  - `ThimbleStatus(id=ActuationPoint.Index, connected=True, statusCode=0, errorDesc="")`  
  - `ThimbleStatus(id=ActuationPoint.Thumb, connected=True, statusCode=0, errorDesc="")`  

#### `ThimbleStatus` fields:
- `id`: `ActuationPoint` → `ActuationPoint.Palm`  
- `connected`: `bool` → `True`  
- `statusCode`: `int` → `0`  
- `errorDesc`: `str` → `""`  

You can get device status by asking it anytime or using appropriate callbacks that are called when the status changes.

### Usage example
#### Asking for the status anytime
```py
# Create a listener to receive status from device
devListener = DeviceStatusListener()
# Add the listener to the client
client.AddMessageListener(devListener)
# Ask for the status
devStatus = devListener.LastStatus()
# Use status informations
print("Last status updated at: " + str(devStatus.timestamp))
print("There are " + str(devStatus.devices.len()) + " connected devices")
if devStatus.devices.len() > 0:
	for device in devStatus.devices:
		print("Device MAC address is: " + str(device.macAddress))
		print("Device hand side is: " + str(device.handSide))
		print("Device battery level is: " + str(device.batteryLevel))
```

#### Using callbacks
```py
# Create an appropriare callback
def deviceStatusUpdateCallback(status):
	print("Device status updated at: " + str(status.timestamp))
	print("There are " + str(len(status.devices)) + " connected devices")
	if len(status.devices) > 0:
		for device in status.devices:
			print("Device MAC address is: " + str(device.macAddress))
			print("Device hand side is: " + str(device.handSide))
			print("Device battery level is: " + str(device.batteryLevel))

# Create a listener to receive status from device
devListener = DeviceStatusListener()
# Add the callback to the listener
devListener.AddStatusCallback(deviceStatusUpdateCallback)
# Add the listener to the client
client.AddMessageListener(devListener)
```

## TDProStatusListener
This object represents the status of the TouchDIVER PRO device(s).\
**⚠️ Important:** This object is only compatible with TouchDIVER PRO, use the DeviceStatusListener for other devices.\
Device status includes the following information:
* **timestamp**: the timestamp of the last received status update message
* **devices**: the list of connected devices' status

Each device status includes the following information:
* **mac address**: the MAC address of the device
* **handSide**: the side of the device
* **signal strength**: the signal strength of the device (in dBm)
* **master status**: the status of the master device
* **slave status**: the list of slave devices' status

Master status includes the following information:
* **battery level**: the battery level of the device
* **charging**: whether the device is charging or not
* **charge complete**: whether the charging is complete or not
* **connection**: a connection status
* **IMU fault**: whether the master IMU is faulty or not
* **ADC fault**: whether the master ADC is faulty or not
* **button pushed**: whether the button is pushed or not

Connection status includes the following information:
* **Bluetooth ON**: whether the Bluetooth is ON or not
* **Bluetooth connected**: whether the device is connected using Bluetooth or not
* **Wi-Fi ON**: whether the Wi-Fi is ON or not
* **Wi-Fi connected**: whether the device is connected using Wi-Fi or not
* **USB connected**: whether the device is connected using USB or not

Each slave status includes the following information:
* **ID**: the ID of the thimble (e.g. "Thumb", "Annular", ect.)
* **IMU fault**: whether the thimble IMU is faulty or not
* **ADC fault**: whether the thimble ADC is faulty or not
* **ToF fault**: whether the thimble Time-of-Flight is faulty or not

#### An example of a `TDProStatusUpdate` object:

- `timestamp`: `int` → `1712136792`  
- `devices`: `List[G2DeviceStatus]` →  
  - `G2DeviceStatus(macAddress="00:1A:7D:DA:71:15", handSide=HandSide.LEFT, signalStrength=-60.5, master=G2MasterStatus(batteryLevel=90, charging=False, chargeCompleted=False, connection=G2ConnectionStatus(bluetoothOn=True, bluetoothConnected=True, wifiOn=False, wifiConnected=False, usbConnected=False), imuFault=False, adcFault=False, buttonPushed=False), nodes=[G2NodeStatus(id=ActuationPoint.Palm, connected=True, imuFault=False, adcFault=False, tofFault=False)])`

#### `G2DeviceStatus` fields:
- `macAddress`: `str` → `"00:1A:7D:DA:71:15"`  
- `handSide`: `HandSide` → `HandSide.LEFT`  
- `signalStrength`: `float` → `-60.5`  
- `master`: `G2MasterStatus` →  
  - `batteryLevel`: `int` → `90`  
  - `charging`: `bool` → `False`  
  - `chargeCompleted`: `bool` → `False`  
  - `connection`: `G2ConnectionStatus` →  
    - `bluetoothOn`: `bool` → `True`  
    - `bluetoothConnected`: `bool` → `True`  
    - `wifiOn`: `bool` → `False`  
    - `wifiConnected`: `bool` → `False`  
    - `usbConnected`: `bool` → `False`  
  - `imuFault`: `bool` → `False`  
  - `adcFault`: `bool` → `False`  
  - `buttonPushed`: `bool` → `False`  
- `nodes`: `List[G2NodeStatus]` →  
  - `G2NodeStatus(id=ActuationPoint.Palm, connected=True, imuFault=False, adcFault=False, tofFault=False)`

#### `G2ConnectionStatus` fields:
- `bluetoothOn`: `bool` → `True`  
- `bluetoothConnected`: `bool` → `True`  
- `wifiOn`: `bool` → `False`  
- `wifiConnected`: `bool` → `False`  
- `usbConnected`: `bool` → `False`  

#### `G2MasterStatus` fields:
- `batteryLevel`: `int` → `90`  
- `charging`: `bool` → `False`  
- `chargeCompleted`: `bool` → `False`  
- `connection`: `G2ConnectionStatus` →  
  - `bluetoothOn`: `bool` → `True`  
  - `bluetoothConnected`: `bool` → `True`  
  - `wifiOn`: `bool` → `False`  
  - `wifiConnected`: `bool` → `False`  
  - `usbConnected`: `bool` → `False`  
- `imuFault`: `bool` → `False`  
- `adcFault`: `bool` → `False`  
- `buttonPushed`: `bool` → `False`  

#### `G2NodeStatus` fields:
- `id`: `ActuationPoint` → `ActuationPoint.Palm`  
- `connected`: `bool` → `True`  
- `imuFault`: `bool` → `False`  
- `adcFault`: `bool` → `False`  
- `tofFault`: `bool` → `False`  


### Usage example
#### Asking for the status anytime
```py
# Create a listener to receive status from device
tdProStatusListener = TDProStatusListener()
# Add the listener to the client
client.AddMessageListener(tdProStatusListener)
# Ask for the status
tdProStatus = tdProStatusListener.LastStatus()
# Use status informations
print("Last status updated at: " + str(tdProStatus.timestamp))
print("There are " + str(tdProStatus.devices.len()) + " connected devices")
if tdProStatus.devices.len() > 0:
	for device in tdProStatus.devices:
		print("Device MAC address is: " + str(device.macAddress))
		print("Device hand side is: " + str(device.handSide))
		print("Device signal strength is: " + str(device.signalStrength))
		print("Device battery level is: " + str(device.master.batteryLevel))
```

#### Using callbacks
```py
# Create an appropriare callback
def tdProStatusUpdateCallback(status):
	print("Device status updated at: " + str(status.timestamp))
	print("There are " + str(len(status.devices)) + " connected devices")
	if len(status.devices) > 0:
		for device in status.devices:
			print("Device MAC address is: " + str(device.macAddress))
			print("Device hand side is: " + str(device.handSide))
			print("Device signal strength is: " + str(device.signalStrength))
			print("Device battery level is: " + str(device.master.batteryLevel))

# Create a listener to receive status from device
tdProStatusListener = TDProStatusListener()
# Add the callback to the listener
tdProStatusListener.AddStatusCallback(tdProStatusUpdateCallback)
# Add the listener to the client
client.AddMessageListener(tdProStatusListener)
```

## WeArtTrackingCalibration
This object represents the calibration procedure of the TouchDIVER device(s).
Calibration is mandatory before starting the use of the device(s).
In order to correctly calibrate the device(s), it's necessary to follow the calibration procedure:
1. Create a WeArtTrackingCalibration object
```py
calibration = WeArtTrackingCalibration()
```
2. (Optional) Add a calibration status and result callbacks
```py
calibration.AddStatusCallback(yourStatusCallback)
calibration.AddResultCallback(yourResultCallback)
```
3. Start the calibration procedure
```py
calibration.Start()
```
**⚠️ Important:** During the calibration process, the user must hold their hand in the correct position as still as possible.

Once started, the calibration procedure will take a few seconds to complete.
You can check the calibration status and result polling the object with getStatus and getResult methods or wait for the callbacks to be called.
Calibration statuses are:
* IDLE: the calibration process has started but is not yet running.
* Calibrating: the calibration process is running, the user has to keep the hand still.
* Running: the calibration process has successfully completed.

### Usage example

##### Polling the object:
```py
while(not calibration.getResult()):
        time.sleep(1)
```

##### Using callbacks:
```py
calibrationFinished = threading.Event()

def calibrationStatusCallback(handside, status):
        print(f"Calibration status for {str(handside)} hand is {str(status)}")

def calibrationResultCallback(handside, result):
	# result == True means that the calibration has successfully finished
	if(result):
		print(f"Calibration successfully completed for {str(handside)} hand!")
		# Set the event to signal the calibration is finished
		calibrationFinished.set()

calibration = WeArtTrackingCalibration()
calibration.AddStatusCallback(calibrationStatusCallback)
calibration.AddResultCallback(calibrationResultCallback)
client.AddMessageListener(calibration)

print("Starting calibration...")
calibration.Start()

# Wait for the calibration event to be set
calibrationFinished.wait() 
print("Calibration finished!")
```

You can stop the calibration procedure anytime by calling the Stop() method.
```py
client.StopCalibration()
```

## TouchEffect
This object represents an effect that can be applied to an haptic object.
An effect can be force, texture, temperature or a combination of them.

### Usage example

#### Creating a touch effect from scratch
```py
# Temperature properties
temperature = WeArtTemperature()
temperature.active = True
temperature.value = 0.1
# Force properties
force = WeArtForce()
force.active = True
force.value = 0.8
# Textures properties
tex = WeArtTexture()
tex.active = True
tex.textureType = WeArtCommon.TextureType.Aluminium
tex.textureVelocity = 0.5
tex.volume = 100
# Create the effect
touchEffect = TouchEffect(temperature, force, tex)
```

#### Modifying an existing touch effect
```py
# Change temperature value
temperature.value = 0.5
# Change force value
force.active = False
# Change texture type
tex.active = False
# Set new values to the touch effect
touchEffect.Set(temperature, force, tex)
```


## WeArtHapticObject
This object represents an haptic object. Haptic objects are the objects that can be actuated by the devices.
An haptic object has an hand side and one or more actuation points.
On an haptic object, you can actuate force, texture, and temperature.

### Usage example

#### Creating an haptic object and apply an effect to it

```py
# Create a haptic object and connect it to the client
hapticObject = WeArtHapticObject(client)
# Set the hand side
hapticObject.handSideFlag = HandSide.Right.value
# Set the actuation point
hapticObject.actuationPointFlag = ActuationPoint.Index
# Add an effect to the actuation point
hapticObject.AddEffect(touchEffect)
```

#### Remove an effect from the haptic object
```py
# Remove the effect from the haptic object
hapticObject.RemoveEffect(touchEffect)
```

## WeArtThimbleTrackingObject
This object represents a thimble tracking object to get closure and abduction data of the thimble(s).
Closures and abductions are represented by a value between 0 and 1, in which 0 means the thimble is fully opened/adducted and 1 means the thimble is fully closed/abducted.

**⚠️ Important:** Thumb has both closure and abduction values populated, while the other fingers have only closure value.

### Usage example

#### Getting closure and abduction values:
```py
# Create a thimble tracking object for the thumb
thumbThimbleTracking = WeArtThimbleTrackingObject(HandSide.Right, ActuationPoint.Thumb)
# Add the thimble tracking object to the client
client.AddThimbleTracking(thumbThimbleTracking)

# Create a thimble tracking object for the index
indexThimbleTracking = WeArtThimbleTrackingObject(HandSide.Right, ActuationPoint.Index)
# Add the thimble tracking object to the client
client.AddThimbleTracking(indexThimbleTracking)

# Poll the thimble tracking object for 10 seconds
for _ in range(100):
	thumbClosure = thumbThimbleTracking.GetClosure()
	thumbAbduction = thumbThimbleTracking.GetAbduction()
	print("Thumb closure: ", thumbClosure)
	print("Thumb abduction: ", thumbAbduction)

	indexClosure = indexThimbleTracking.GetClosure()
	print("Index closure: ", indexClosure)

	time.sleep(0.1)
```

## WeArtTrackingRawData
This object represents the raw sensors data received from the thimble(s).
Raw data are:
* 3-axis accelerometer [expressed in 'g']
* 3-axis gyroscope [expressed in 'deg/s']
* Time of Flight sensor <b>(not available for TouchDIVER Pro)</b> [expressed in millimetres between the finger and palm]

**⚠️ Important:** Time-of-flight data are not available for TouchDIVER Pro devices as they don't have a time-of-flight sensor installed.

### Usage example
#### Getting raw data from thumb:
```py
# Create a thimble tracking raw data for the thumb
trackingRawSensorData = WeArtTrackingRawData(HandSide.Right, ActuationPoint.Thumb)
# Add the thimble tracking raw data object as a listener to handle raw data messages coming from the Middleware or WEART-App
client.AddMessageListener(trackingRawSensorData)
# Activates raw data transmission from the Middleware or WEART-App
client.StartRawData()

# Wait for the first sample to be received
ts = trackingRawSensorData.GetLastSample().timestamp
while ts == 0:
	time.sleep(0.1)
	ts = trackingRawSensorData.GetLastSample().timestamp

# Poll the thimble tracking raw data for 10 seconds
for _ in range (100):
	thumbRawData = trackingRawSensorData.GetLastSample().data
	thumbAccData = thumbRawData.accelerometer
	thumbGyroData = thumbRawData.gyroscope
	thumbToFData = thumbRawData.timeOfFlight
	print("THUMB ACC X, Y, Z:", thumbAccData.x, thumbAccData.y, thumbAccData.z)
	print("THUMB GYRO X, Y, Z:", thumbGyroData.x, thumbGyroData.y, thumbGyroData.z)
	print("THUMB TOF:", thumbToFData.distance)
	time.sleep(0.1)

# Stop raw data streaming
client.StopRawData()
```

## WeArtAnalogSensorData
This object represents the analog sensors data received from the thimble(s).
Analog sensors are the sensors that measure the pressure applied to and the temperature of the thimble(s).

**⚠️ Important:** Analog sensors are not available for TouchDIVER Pro device(s).

### Usage example

#### Getting analog data from thumb:
```py
# Create a thimble tracking analog data for the thumb
thumbAnalogSensorData = WeArtAnalogSensorData(HandSide.Right, ActuationPoint.Thumb)
# Add the thimble tracking analog data object as a listener to handle analog data messages coming from the Middleware or WEART-App
client.AddMessageListener(thumbAnalogSensorData)

# Wait for the first sample to be received
ts = analogSensorData.GetLastSample().timestamp
while ts == 0:
	time.sleep(1)
	ts = analogSensorData.GetLastSample().timestamp

# Poll the thimble tracking analog data for 10 seconds
for _ in range (100):
	thumbAnalogData = analogSensorData.GetLastSample().data
	thumbNTCRawData = thumbAnalogData.ntcTemperatureRaw
	thumbNTCConvertedData = thumbAnalogData.ntcTemperatureConverted
	thumbForceRawData = thumbAnalogData.forceSensingRaw
	thumbForceConvertedData = thumbAnalogData.forceSensingConverted

	print("THUMB TEMP RAW:", thumbNTCRawData)
	print("THUMB TEMP CONV:", thumbNTCConvertedData)
	print("THUMB FORCE RAW:", thumbForceRawData)
	print("THUMB FORCE CONV:", thumbForceConvertedData)
	
	time.sleep(0.1)
```

# Acknowledgements
A special thank you for the support and collaboration in the realization of this SDK porting to [Emanuele De Santis](https://github.com/trunk96), Department of Computer, Control and Management Engineering "Antonio Ruberti" - Sapienza University of Rome. This work was partially supported by Rome Technopole, FP4, through
the project “Phygital Twin Technologies for innovative Surgical Training and Planning”.

# Copyright
Copyright &copy; 2025 Weart S.r.l.
