from WeArtHapticObject import WeArtHapticObject
from WeArtCommon import HandSide, ActuationPoint, CalibrationStatus
from WeArtTemperature import WeArtTemperature
from WeArtTexture import WeArtTexture
from WeArtForce import WeArtForce
from WeArtCommon import TextureType
from WeArtEffect import TouchEffect
from WeArtTrackingCalibration import WeArtTrackingCalibration
from WeArtThimbleTrackingObject import WeArtThimbleTrackingObject
from WeArtTrackingRawData import WeArtTrackingRawData
from MiddlewareStatusListener import MiddlewareStatusListener
from WeArtAnalogSensorData import WeArtAnalogSensorData

from WeArtClient import WeArtClient
import WeArtCommon
import time

if __name__ == '__main__':
    client = WeArtClient(WeArtCommon.DEFAULT_IP_ADDRESS, WeArtCommon.DEFAULT_TCP_PORT)
    client.Run()
    client.Start()


    mwListener = MiddlewareStatusListener()
    client.AddMessageListener(mwListener)

    #calibration = WeArtTrackingCalibration()
    #client.AddMessageListener(calibration)
    #client.StartCalibration()

    #while(not calibration.getResult()):
    #    time.sleep(1)
    
    #print("Calibrazione finita")
    #client.StopCalibration()

    
    '''
    hapticObject = WeArtHapticObject(client)
    hapticObject.handSideFlag = HandSide.Right.value
    hapticObject.actuationPointFlag = ActuationPoint.Index | ActuationPoint.Middle
    touchEffect = TouchEffect(WeArtTemperature(), WeArtForce(), WeArtTexture())
    temperature = WeArtTemperature()
    temperature.active = True
    temperature.value = 0.7
    force = WeArtForce()
    force.active = True
    force.value = 0.8
    tex = WeArtTexture()
    tex.active = True
    tex.textureType = TextureType.TextileMeshMedium
    tex.textureVelocity = 0.5
    touchEffect.Set(temperature, force, tex)
    if (len(hapticObject.activeEffects) <= 0):
        hapticObject.AddEffect(touchEffect)
    else:
        hapticObject.UpdateEffects()
    '''

    """thumbThimbleTracking = WeArtThimbleTrackingObject(HandSide.Right, ActuationPoint.Thumb)
    client.AddThimbleTracking(thumbThimbleTracking)

    for i in range(200):
        closure = thumbThimbleTracking.GetClosure()
        abduction = thumbThimbleTracking.GetAbduction()
        print(f"{closure}, {abduction}")
        time.sleep(0.1) """

    """ trackingRawSensorData = WeArtTrackingRawData(HandSide.Right, ActuationPoint.Index)
    client.AddMessageListener(trackingRawSensorData)
    client.StartRawData()

    ts = trackingRawSensorData.GetLastSample().timestamp
    while ts == 0:
        time.sleep(1)
        ts = trackingRawSensorData.GetLastSample().timestamp
    sample = trackingRawSensorData.GetLastSample()
    print(sample)
    client.StopRawData() """
    time.sleep(1)
    #analogSensorData = WeArtAnalogSensorData(HandSide.Right, ActuationPoint.Index)
    #client.AddMessageListener(analogSensorData)
    
    client.Stop()