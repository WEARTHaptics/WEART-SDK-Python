from weartsdk import *
from weartsdk.WeArtCommon import HandSide, ActuationPoint, TextureType
import time
import logging

'''
Sample demo script to show the functionallity of the WEART Python SDK 
'''

if __name__ == '__main__':
    
    # Istantiate TCP/IP client to communicate with the Middleware
    client = WeArtClient(WeArtCommon.DEFAULT_IP_ADDRESS, WeArtCommon.DEFAULT_TCP_PORT, log_level=logging.INFO)
    client.Run()
    client.Start()

    # Listener to receive data status from Middleware
    mwListener = MiddlewareStatusListener()
    client.AddMessageListener(mwListener)

    # Calibration manager 
    calibration = WeArtTrackingCalibration()
    client.AddMessageListener(calibration)
    # Start Calibration Finger tracking algorithm
    client.StartCalibration()

    # Wait for the result
    while(not calibration.getResult()):
        time.sleep(1)
    
    # Stop calibration
    client.StopCalibration()

    
    # Instantiate a HapticObject to provide actuations
    hapticObject = WeArtHapticObject(client)
    hapticObject.handSideFlag = HandSide.Right.value
    hapticObject.actuationPointFlag = ActuationPoint.Index | ActuationPoint.Middle

    # Create an effect with Temperatures, Force and Textures
    touchEffect = TouchEffect(WeArtTemperature(), WeArtForce(), WeArtTexture())
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

    # Istantiate a ThimbeTrackingObject to read closure and abductions value from the thimble
    thumbThimbleTracking = WeArtThimbleTrackingObject(HandSide.Right, ActuationPoint.Thumb)
    client.AddThimbleTracking(thumbThimbleTracking)

    # Read tracking data for 200 iterations
    for i in range(200):
        closure = thumbThimbleTracking.GetClosure()
        abduction = thumbThimbleTracking.GetAbduction()
        print(f"{closure}, {abduction}")
        time.sleep(0.1) 

    
    # Instantiate tracking raw data to read tracking raw data from the thimble's sensors
    trackingRawSensorData = WeArtTrackingRawData(HandSide.Right, ActuationPoint.Index)
    client.AddMessageListener(trackingRawSensorData)
    # Activates raw data transmission
    client.StartRawData()

    # Read sample tracking raw data
    ts = trackingRawSensorData.GetLastSample().timestamp
    while ts == 0:
        time.sleep(1)
        ts = trackingRawSensorData.GetLastSample().timestamp
    sample = trackingRawSensorData.GetLastSample()
    print(sample)

    # Stop raw data streaming
    client.StopRawData()
    
    '''
    # Instantiate Analog Sensor raw data
    # This feature work just enabling the functionality from the Middleware
    # during this condition streaming the WeArtTrackingRawData doesn't work
    analogSensorData = WeArtAnalogSensorData(HandSide.Right, ActuationPoint.Index)
    client.AddMessageListener(analogSensorData)

    # Read sample analog sensor data
    ts = analogSensorData.GetLastSample().timestamp
    while ts == 0:
        time.sleep(1)
        ts = analogSensorData.GetLastSample().timestamp
    sample = analogSensorData.GetLastSample()
    print(sample)
    '''

    
    # Stop client and close the commnunication with the Middleware
    client.Stop()
    client.Close()