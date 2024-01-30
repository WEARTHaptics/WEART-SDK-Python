from WeArtHapticObject import WeArtHapticObject
from WeArtCommon import HandSide, ActuationPoint, CalibrationStatus
from WeArtTemperature import WeArtTemperature
from WeArtTexture import WeArtTexture
from WeArtForce import WeArtForce
from WeArtCommon import TextureType
from WeArtEffect import TouchEffect
from WeArtTrackingCalibration import WeArtTrackingCalibration

from WeArtClient import WeArtClient
import WeArtCommon
import time

if __name__ == '__main__':
    client = WeArtClient(WeArtCommon.DEFAULT_IP_ADDRESS, WeArtCommon.DEFAULT_TCP_PORT)
    client.Run()
    client.Start()

    calibration = WeArtTrackingCalibration()
    client.AddMessageListener(calibration)
    client.StartCalibration()

    hand = calibration.getCurrentHand()
    status = calibration.getStatus()
    result = calibration.getResult()
    print(hand, status, result)
    
    # Be notified by callbacks when the calibration status changes
    def prova(hand:HandSide, status:CalibrationStatus):
        print(f"Aggiornamento sullo stato: {status}")

    def prova2(hand:HandSide, result:bool):
        print(f"Risultato pronto: {result}")

    calibration.AddStatusCallback(prova)
    
    # Be notified by callbacks when a calibration result is available
    calibration.AddResultCallback(prova2)

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
    time.sleep(10)

    client.StopCalibration()
    hand = calibration.getCurrentHand()
    status = calibration.getStatus()
    result = calibration.getResult()
    print(hand, status, result)
    
    client.Stop()