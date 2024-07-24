# Weart Low-Level Python SDK

The Weart Low-Level Python SDK  allows to connect to the WEART Middleware (dekstop application) and perform various actions with the TouchDIVER devices:
* Start and Stop the middleware operations
* Calibrate the device
* Receive tracking data from the devices
* Receive raw data from the thimble's motion sensors 
* Receive analog raw data from the thimble's senosrs
* Send haptic effects to the devices

## Documentations, SDKs and other resources
WEART Download page [here](https://weart.it/developer-guide/)

# Acknowledgements

A special thank you for the support and collaboration in the realization of this SDK porting to [Emanuele De Santis](https://github.com/trunk96), Department of Computer, Control and Management Engineering "Antonio Ruberti" - Sapienza University of Rome. This work was partially supported by Rome Technopole, FP4, through
the project “Phygital Twin Technologies for innovative Surgical Training and Planning”.

# Setup
The minimum setup to use the weart SDK consists of:
* A PC with the Middleware installed
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

# Example script
In the repository you will find a *test.py* script with all the snippets you need to work with the WEART SDK

# Features

## Start/Stop Client
Once connected to the middleware, it's still not possible to receive tracking data and send haptic commands to the devices.
In order to do so, it's important to start the middleware with the proper command.

To start the middleware operations, call the Start() method.

```py
client = WeArtClient(WeArtCommon.DEFAULT_IP_ADDRESS, WeArtCommon.DEFAULT_TCP_PORT)
client.Run()
client.Start()
```

To stop the middleware, call the Stop() method.

```py
client.Stop();
```

## Devices calibration
After starting the communication with the middleware, it's now possible to calibrate the TouchDIVER devices.
The calibration allows to set the initial offsets of each thimble relative to the control unit position, in order to improve the finger tracking output.

First, create the calibration tracking object and add it to the client. The WeArtTrackingCalibration object allows to listen for calibration messages
from the middleware, and get notified when the calibration process ends.

```py
calibration = WeArtTrackingCalibration()
client.AddMessageListener(calibration)
# Start Calibration Finger tracking algorithm
client.StartCalibration()
```

Then, start the calibration procedure. This will allow the middleware to calibrate the hand sensor offsets based on the current setup (thimbles and control device position, hand inclination, personal differences in the fingers etc..).

```py
client.StartCalibration()
```

It’s possible to get the calibration status and result from the tracker object itself, or through callbacks

```py
calibration.getResult()
```

You can stop the calibration anytime

```py
client.StopCalibration()
```

## Haptic feedback

The TouchDIVER allows to perform haptic feedback on the user's finger through its *thimbles*.
Every thimble can apply a certain amount of pressure, temperature and vibration based on the processed object and texture.

### Haptic Object

A WeArtHapticObject is the basic object used to apply haptic feedback.
To create one, use the following code:

```{.cpp}
hapticObject = WeArtHapticObject(client)
hapticObject.handSideFlag = HandSide.Right.value
hapticObject.actuationPointFlag = ActuationPoint.Index | ActuationPoint.Middle
```


### Create Effect

The SDK contains a basic TouchEffect class to apply effects to the haptic device.
The TouchEffect class contains the effects without any processing.
For different use cases (e.g. values not directly set, but computed from other parameters), create a different effect class by implementing the TouchEffect interface.

Create the object on which the temperature, force and texture values will be applied:

```{.cpp}
touchEffect = TouchEffect(WeArtTemperature(), WeArtForce(), WeArtTexture())
```

### Add or Update Effect

It's possible to add a new effect to an haptic object, or to update an existing one.

In the example below, the effect created in the previous section is updated with a new temperature, force and texture.
It is then added to the haptic object if not already present, otherwise the haptic object is updated in order to send the new 
effect parameters to the middleware and then to the device.

```py
# Temperature properties
temperature = WeArtTemperature()
temperature.active = True
temperature.value = 0.7
# Force properties
force = WeArtForce()
force.active = True
force.value = 0.8
# Textures properties
tex = WeArtTexture()
tex.active = True
tex.textureType = TextureType.TextileMeshMedium
tex.textureVelocity = 0.5 # maximum value
# Set Effect effect properties
touchEffect.Set(temperature, force, tex)
if (len(hapticObject.activeEffects) <= 0):
    hapticObject.AddEffect(touchEffect) #Add effect if there is not any
else:
    # Update the effect over time
    hapticObject.UpdateEffects()
```

@note When multiple effects are added to a WeArtHapticObject, which effect is applied depends on the order in which the effects are added. In particular, for each value (temperature, force, texture) only the latest active one will be applied.

### Remove Effect

If an effect is not needed anymore, it can be removed from the haptic object with the *RemoveEffect* method.

```py
hapticObject.RemoveEffect(touchEffect)
```

## Tracking

After starting the middleware and performing the device calibration, it's possible to receive tracking data
related to the TouchDIVER thimbles.

To read these values, create and set a thimble tracker object for monitoring the closure/abduction value of a given finger:
```py
thumbThimbleTracking = WeArtThimbleTrackingObject(HandSide.Right, ActuationPoint.Thumb)
client.AddThimbleTracking(thumbThimbleTracking)
```

Once this object is added to the client, it will start receiving the tracking values.
To access the closure and abduction values, simply use the getters provided by the thimble tracking object.

The closure value ranges from 0 (opened) to 1 (closed).

The abduction value ranges from 0 (finger near the hand's central axis) to 1 (finger far from the hand central axis).

```py
closure = thumbThimbleTracking.GetClosure()
abduction = thumbThimbleTracking.GetAbduction()
```

@note The **closure** value is available for all thimbles, while the **abduction** value is available only for the thumb (other thimbles will have a value of 0).

## Tracking Raw Data

It's possible to receive the raw data from the tracking sensors on each thimble (and the control unit), in addition to the tracking data.
Each sensor has:
* 3-axis accelerometer
* 3-axis gyroscope
* Time of Flight sensor

To read these values, create a WeArtTrackingRawData object and add it to the client.
```py
trackingRawSensorData = WeArtTrackingRawData(HandSide.Right, ActuationPoint.Index)
client.AddMessageListener(trackingRawSensorData)
```

Once this object is added to the client, it will listen for raw data messages.
To start receiving raw data from the middleware, call the client.StartRawData() method.
To stop receiving raw data, call the client.StopRawData() method.

To get the sensors data, get the latest sample (WeArtTrackingRawData::Sample) from the WeArtTrackingRawData object.
The sample contains the accelerometer, gyroscope and time of flight data, in addition to the timestamp of its sampling (generated by the middleware and represented as milliseconds in unix epoch time).
```py
ts = trackingRawSensorData.GetLastSample().timestamp 
sample = trackingRawSensorData.GetLastSample()
accX = sample.data.accelerometer.x
accY = sample.data.accelerometer.y
accZ = sample.data.accelerometer.z
```

@note The Palm (control unit) doesn't contain a Time-Of-Flight sensor, so its value is always set to 0.

In addition to getting the latest sample by polling the tracking object, it's possible to add a callback called whenever a new sensor data sample is
received from the TouchDIVER.

## Analog Raw Sensors Data

It's possible to receive the raw data from the sensors on each thimble (and the control unit), instead of the tracking data when this function is activated on the Middleware.
Each sensor has:
* NTC - Negative Temperature Coefficient (raw data and converted degree)
* FSR - force sensing resistor (raw adata and converted newton)

To read these values, create a WeArtAnalogSensorData object and add it to the client.
```py
analogSensorData = WeArtAnalogSensorData(HandSide.Right, ActuationPoint.Index)
client.AddMessageListener(analogSensorData)
```

Once this object is added to the client, it will listen for raw data messages as soon the Middleware is on start.

To get the sensors data, get the latest sample.

```py
ts = analogSensorData.GetLastSample().timestamp
sample = analogSensorData.GetLastSample()
forceSensingRaw = sample.data.forceSensingRaw
```

@note The Palm (control unit) doesn't contain a analog sensor, so its value is always set to 0.



## Middleware and Devices status tracking

The SDK allows to track and receives updates about the middleware and the connected devices status.

In particular, the information is available through a MiddlewareStatusListener object, that must be added as listener to the client object:
```py
mwListener = MiddlewareStatusListener()
client.AddMessageListener(mwListener)
```

The MiddlewareListener tracks the messages from the middleware, saving and notifying about status changes.
In particular, it's possible to register callbacks for the middleware and devices status.

The status callback will receive a struct with the MiddlewareStatusUpdate type, which includes:
* Middleware version
* Middleware status (MiddlewareStatus)
* Status code and description  
* Whether actuations are enabled or not
* List of the connected devices. For each device:
	* Mac Address
	* Assigned HandSide
	* Overall battery level
	* Status of each thimble (actuation point, connected or not, status code etc..)

The same information can be asked to the MiddlewareListener (in polling fashion) by calling the *mwListener.lastStatus()* method.

### Status Codes
The MiddlewareListener object allows to get the middleware status, which includes the latest status code sent by the middleware while performing
its operations.

The current status codes (along with their description) are:

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
| 300 | STOP_GENERIC_ERROR | Generic error occurred while stopping session |

@note The description of each status code might change between different Middleware versions, use the status code to check instead of the description.

## Copyright

Copyright &copy; 2024 Weart S.r.l.
