"""
This script communicates with a WeArt device using the WeArt SDK, employing a polling-based approach instead of callbacks. 
It connects to the middleware via TCP/IP, monitors device status, and performs calibration before capturing tracking data. 
It continuously queries the middleware and device statuses, waiting for events like device connection and calibration completion.

Main functionalities:
- Uses polling to check device connection and calibration status.
- Retrieves and prints thimble tracking and raw sensor data.
- Applies haptic effects (temperature, force, texture) to the device.
- Ensures proper cleanup of connections and resources before exiting.
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

    # Listener to receive data status from Middleware
    mwListener = MiddlewareStatusListener()
    client.AddMessageListener(mwListener)

    # Listener to receive data status from Device(s)
    tdpListener = TDProStatusListener()
    client.AddMessageListener(tdpListener)

    # Polling the middleware status until at least a device is connected
    middlewareStatus = mwListener.LastStatus()
    if len(middlewareStatus.connectedDevices) == 0:
        print("Waiting for device to be connected...")
        while len(middlewareStatus.connectedDevices) == 0:
            time.sleep(0.5)
            middlewareStatus = mwListener.LastStatus()

    # Get device(s) informations
    deviceStatus = tdpListener.LastStatus()
    for i, device in enumerate(deviceStatus.devices):
        print(f"Device {i} connected with MAC address {device.macAddress}, hand side {device.handSide} has battery at {device.master.batteryLevel}%")
        print(f"Device {i} sensors last calibrated at {device.sensorsCalibDate}")

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
        
        thumb_acc = thumbSampleData.accelerometer
        thumb_gyro = thumbSampleData.gyroscope

        print(f"THUMB:\n\tAcc:\n\t\tX: {thumbSampleData.accelerometer.x}\n\t\tY: {thumbSampleData.accelerometer.y}\n\t\tZ: {thumbSampleData.accelerometer.z}\n\tGyro:\n\t\tX: {thumbSampleData.gyroscope.x}\n\t\tY: {thumbSampleData.gyroscope.y}\n\t\tZ: {thumbSampleData.gyroscope.z}")

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
                                        WeArtCommon.ActuationPoint.Middle | \
                                        WeArtCommon.ActuationPoint.Annular | \
                                        WeArtCommon.ActuationPoint.Pinky | \
                                        WeArtCommon.ActuationPoint.Palm

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