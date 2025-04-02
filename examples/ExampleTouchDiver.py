"""
This script initializes and manages a WeArt haptic interaction session using the WeArt SDK.  
It establishes a TCP/IP connection with the WeArt Middleware, monitors device statuses, and collects sensor data,  
including tracking and raw sensor values. Additionally, it applies haptic effects such as temperature, force, and texture  
to the connected devices.  

Main functionalities:
- Connects to the WeArt Middleware via TCP/IP.
- Listens for middleware and device status updates.
- Waits for at least one device to be connected.
- Calibrates finger tracking for the connected device(s).
- Retrieves and prints thumb and index finger tracking data.
- Streams raw sensor data from the thimble sensors.
- Applies haptic effects (temperature, force, texture) to the device(s).
- Manages the activation and deactivation of haptic effects.
- Gracefully stops devices and closes the TCP/IP connection upon termination.  

"""

import logging
import time
import sys, os

sys.path.append(os.path.abspath(".."))
from weartsdk import *

if __name__ == '__main__':
    
    # Istantiate TCP/IP client to communicate with the Middleware
    client = WeArtClient(WeArtCommon.DEFAULT_IP_ADDRESS, WeArtCommon.DEFAULT_TCP_PORT, log_level=logging.INFO)
    client.Run()

    # Listener to receive status from Middleware
    mwListener = MiddlewareStatusListener()
    client.AddMessageListener(mwListener)

    # Listener to receive status from Device(s)
    dListener = DeviceStatusListener()
    client.AddMessageListener(dListener)

    # Polling the middleware status until at least a device is connected
    middlewareStatus = mwListener.LastStatus()
    if len(middlewareStatus.connectedDevices) == 0:
        print("Waiting for device to be connected...")
        while len(middlewareStatus.connectedDevices) == 0:
            time.sleep(0.5)
            middlewareStatus = mwListener.LastStatus()

    # Get device(s) informations
    deviceStatus = dListener.LastStatus()
    for i, device in enumerate(deviceStatus.devices):
        print(f"Device {i} connected with MAC address {device.macAddress}, hand side {device.handSide} has battery at {device.batteryLevel}%")

    # Start the device(s)
    client.Start()

    input("Wear the device(s) and press Enter to start calibration...")

    # Calibration manager 
    calibration = WeArtTrackingCalibration()
    client.AddMessageListener(calibration)
    # Start Calibration Finger tracking algorithm
    client.StartCalibration()

    # Polling for calibration result
    while(not calibration.getResult()):
        time.sleep(1)
    
    # Stop calibration
    client.StopCalibration()

    # Istantiate a ThimbeTrackingObject to read closure and abductions value from the thumb
    thumbThimbleTracking = WeArtThimbleTrackingObject(WeArtCommon.HandSide.Right, WeArtCommon.ActuationPoint.Thumb)
    # Add the thimble tracking object to the client
    client.AddThimbleTracking(thumbThimbleTracking)
    # Istantiate a ThimbeTrackingObject to read closure value from the index
    indexThimbleTracking = WeArtThimbleTrackingObject(WeArtCommon.HandSide.Right, WeArtCommon.ActuationPoint.Index)
    # Add the thimble tracking object to the client
    client.AddThimbleTracking(indexThimbleTracking)

    # Print abduction and closure values for 10 seconds
    for _ in range(20):
        print("THUMB ABDUCTION: " + str(thumbThimbleTracking.GetAbduction()))
        print("THUMB CLOSURE: " + str(thumbThimbleTracking.GetClosure()))
        # Only thumb has abduction values, so for index print only closure
        print("IDEX CLOSURE: " + str(indexThimbleTracking.GetClosure()))
        time.sleep(0.5)

    # Instantiate tracking raw data to read tracking raw data from the thimble's sensors
    thumbRawSensorData = WeArtTrackingRawData(WeArtCommon.HandSide.Right, WeArtCommon.ActuationPoint.Thumb)
    client.AddMessageListener(thumbRawSensorData)

    # Activates raw data transmission
    client.StartRawData()

    # Wait until the first sample is received
    ts = thumbRawSensorData.GetLastSample().timestamp
    while ts == 0:
        time.sleep(1)
        ts = thumbRawSensorData.GetLastSample().timestamp
    
    # Print raw data for 10 seconds
    for _ in range (20):
        thumbSampleData = thumbRawSensorData.GetLastSample().data
        print(f"THUMB:\n\tAcc:\n\t\tX: {thumbSampleData.accelerometer.x}\n\t\tY: {thumbSampleData.accelerometer.y}\n\t\tZ: {thumbSampleData.accelerometer.z}\n\tGyro:\n\t\tX: {thumbSampleData.gyroscope.x}\n\t\tY: {thumbSampleData.gyroscope.y}\n\t\tZ: {thumbSampleData.gyroscope.z}\n\tToF: {thumbRawSensorData.timeOfFlight.distance}")
        time.sleep(0.5)

    # Stop raw data streaming
    client.StopRawData()
    
    # Create a temperature object
    myTemperature = WeArtTemperature()
    myTemperature.active = True
    myTemperature.value = 0.2
    
    # Create a force object
    myForce = WeArtForce()
    myForce.active = True
    myForce.value = 0.8
    
    # Create a texture object
    myTexture = WeArtTexture()
    myTexture.active = True
    myTexture.textureType = WeArtCommon.TextureType.Aluminium
    myTexture.textureVelocity = 0.5
    myTexture.volume = 100

    # Create a TouchEffect object
    myTouchEffect = TouchEffect(myTemperature, myForce, myTexture)

    # Create an HapticObject bonded to the client
    myHapticObject = WeArtHapticObject(client)

    # Set the HapticObject hand side and actuation points
    myHapticObject.handSideFlag = WeArtCommon.HandSide.Right
    myHapticObject.actuationPointFlag = WeArtCommon.ActuationPoint.Thumb | \
                                        WeArtCommon.ActuationPoint.Index | \
                                        WeArtCommon.ActuationPoint.Middle

    # Add the TouchEffect to the HapticObject
    myHapticObject.AddEffect(myTouchEffect)

    # Keep the effect active for 5 seconds
    time.sleep(5)

    # Remove the effect
    myHapticObject.RemoveEffect(myTouchEffect)

    # Keep the effect inactive for 1 second
    time.sleep(1)

    # Stop device(s)
    client.Stop()

    # Close TCP/IP connection
    client.Close()