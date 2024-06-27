from .WeArtClient import WeArtClient
from .WeArtMessages import WeArtMessage, StopTemperatureMessage, StopForceMessage, StopTextureMessage
from .WeArtMessages import SetTemperatureMessage, SetForceMessage, SetTextureMessage
from .WeArtEffect import WeArtEffect
from .WeArtCommon import HandSide, ActuationPoint
from . import WeArtCommon
from .WeArtForce import WeArtForce
from .WeArtTemperature import WeArtTemperature
from .WeArtTexture import WeArtTexture

class WeArtHapticObject:
    def __init__(self, client:WeArtClient):
        self.handSideFlag = None
        self.actuationPointFlag = None
        self.weArtTemperature = None
        self.weArtForce = None
        self.weArtTexture = None
        self.activeEffects = []
        self.__client = client

    def AddEffect(self, effect:WeArtEffect):
        if not self.ContainsEffect(effect):
            self.activeEffects.append(effect)
            self.UpdateEffects()

    def RemoveEffect(self, effect:WeArtEffect):
        if self.ContainsEffect(effect):
            self.activeEffects.remove(effect)
            self.UpdateEffects()

    def ContainsEffect(self, effect:WeArtEffect):
        if effect in self.activeEffects:
            return True
        else:
            return False
        
    def UpdateEffects(self):
        if len(self.activeEffects) == 0:
            self.weArtForce = WeArtForce(active = False, force = WeArtCommon.defaultForce)
            self.weArtTemperature = WeArtTemperature()
            self.weArtTemperature.active = False
            self.weArtTemperature.value(WeArtCommon.defaultTemperature)
            self.weArtTexture = WeArtTexture(active = False, texture_type=WeArtCommon.defaultTextureIndex, velocity = WeArtTexture.DefaultVelocity)
            msg1 = StopTemperatureMessage()
            self.SendMessage(msg1)
            msg2 = StopForceMessage()
            self.SendMessage(msg2)
            msg3 = StopTextureMessage()
            self.SendMessage(msg3)
        else:
            tempEffect = None
            for effect in self.activeEffects:
                if effect.getTemperature().active:
                    tempEffect = effect
                    break
            
            # update temperature
            newTemp = None
            if tempEffect is None:
                newTemp = WeArtTemperature()
            else:
                newTemp = tempEffect.getTemperature()
            if self.weArtTemperature is None or (not newTemp == self.weArtTemperature):
                if not newTemp.active:
                    msg = StopTemperatureMessage()
                    self.SendMessage(msg)
                else:
                    msg = SetTemperatureMessage(newTemp.value)
                    self.SendMessage(msg)
                self.weArtTemperature = newTemp
            
            # update force
            forceEffect = None
            for effect in self.activeEffects:
                if effect.getForce().active:
                    forceEffect = effect
                    break
            newForce = None
            if forceEffect is not None:
                newForce = forceEffect.getForce()
            else:
                newForce = WeArtForce()
            if self.weArtForce is None or (not (newForce == self.weArtForce)):
                if not (newForce.active):
                    msg = StopForceMessage()
                    self.SendMessage(msg)
                else:
                    fValue = [newForce.value, 0.0, 0.0]
                    msg = SetForceMessage(fValue)
                    self.SendMessage(msg)
                self.weArtForce = newForce

            # update texture
            texEffect = None
            for effect in self.activeEffects:
                if effect.getTexture().active:
                    texEffect = effect
                    break
            newTex = None
            if texEffect is not None:
                newTex = texEffect.getTexture()
            else:
                newTex = WeArtTexture()
            if self.weArtTexture is None or (not (newTex == self.weArtTexture)):
                if not (newTex.active):
                    msg = StopTextureMessage()
                    self.SendMessage(msg)
                else:
                    msg = SetTextureMessage(newTex.textureType, newTex.textureVelocity, newTex.volume)
                    self.SendMessage(msg)
                self.weArtTexture = newTex

    
    def SendMessage(self, msg:WeArtMessage):
        hand_sides = [HandSide.Left, HandSide.Right]
        actuation_points = [ActuationPoint.Thumb, ActuationPoint.Index, ActuationPoint.Middle, ActuationPoint.Palm]
        for hs in hand_sides:
            if hs & self.handSideFlag:
                for ap in actuation_points:
                    if ap & self.actuationPointFlag:
                        msg.setHandSide(hs)
                        msg.setActuationPoint(ap)
                        self.__client.SendMessage(msg)

__all__ = ['WeArtHapticObject']
