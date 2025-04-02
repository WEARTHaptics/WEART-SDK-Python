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
    """
    A class representing a haptic object that interacts with a client to apply effects such as force, temperature, and texture.

    Attributes:
        handSideFlag (HandSide): The hand side flag indicating whether the effect is applied to the left or right hand.
        actuationPointFlag (ActuationPoint): The actuation point flag indicating where the effect is applied (e.g., thumb, index finger).
        weArtTemperature (WeArtTemperature): The temperature effect applied to the haptic object.
        weArtForce (WeArtForce): The force effect applied to the haptic object.
        weArtTexture (WeArtTexture): The texture effect applied to the haptic object.
        activeEffects (list): A list of active effects applied to the haptic object.
        __client (WeArtClient): The client used to send messages to control the effects.

    Methods:
        __init__(self, client: WeArtClient):
            Initializes a WeArtHapticObject with the specified client and default values for its attributes.

        AddEffect(self, effect: WeArtEffect):
            Adds a new effect to the list of active effects if it is not already present.

        RemoveEffect(self, effect: WeArtEffect):
            Removes an effect from the list of active effects if it exists.

        ContainsEffect(self, effect: WeArtEffect):
            Checks if the specified effect is already present in the active effects.

        UpdateEffects(self):
            Updates the effects applied to the haptic object. It checks each active effect and sends appropriate messages 
            (SetTemperatureMessage, SetForceMessage, SetTextureMessage) to update the haptic object, or stops the effect 
            if there are no active effects.

        SendMessage(self, msg: WeArtMessage):
            Sends the specified message to the client, associating it with the correct hand side and actuation point 
            based on the flags.
    """
    def __init__(self, client: WeArtClient):
        """
        Initializes a WeArtHapticObject with the specified client and default values for its attributes.
        
        Parameters:
            client (WeArtClient): The client used to send messages to control the effects.
        """
        self.handSideFlag = None
        self.actuationPointFlag = None
        self.weArtTemperature = None
        self.weArtForce = None
        self.weArtTexture = None
        self.activeEffects = []
        self.__client = client

    def AddEffect(self, effect: WeArtEffect):
        """
        Adds a new effect to the list of active effects (if it is not already present).

        Parameters:
            effect (WeArtEffect): The effect to be added to the haptic object.
        """
        if not self.ContainsEffect(effect):
            self.activeEffects.append(effect)
            self.UpdateEffects()

    def RemoveEffect(self, effect: WeArtEffect):
        """
        Removes an effect from the list of active effects (if it exists).

        Parameters:
            effect (WeArtEffect): The effect to be removed from the haptic object.
        """
        if self.ContainsEffect(effect):
            self.activeEffects.remove(effect)
            self.UpdateEffects()

    def ContainsEffect(self, effect: WeArtEffect):
        """
        Checks if the specified effect is already present in the active effects.

        Parameters:
            effect (WeArtEffect): The effect to check for in the active effects.
        
        Returns:
            bool: True if the effect is found in the active effects, False otherwise.
        """
        if effect in self.activeEffects:
            return True
        else:
            return False
        
    def UpdateEffects(self):
        """
        Updates the effects applied to the haptic object. It checks each active effect and sends appropriate messages 
        (SetTemperatureMessage, SetForceMessage, SetTextureMessage) to update the haptic object, or stops the effect 
        if there are no active effects.
        """
        if len(self.activeEffects) == 0:
            self.weArtForce = WeArtForce(active = False, force = WeArtCommon.defaultForce)
            self.weArtTemperature = WeArtTemperature()
            self.weArtTemperature.active = False
            self.weArtTemperature.value = WeArtCommon.defaultTemperature
            self.weArtTexture = WeArtTexture(active = False, texture_type = WeArtCommon.defaultTextureIndex, velocity = WeArtTexture.DefaultVelocity)
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
  
    def SendMessage(self, msg: WeArtMessage):
        """
        Sends the specified message to the client, associating it with the correct hand side and actuation point 
        based on the flags.

        Parameters:
            msg (WeArtMessage): The message to be sent to the client.
        """
        hand_sides = [HandSide.Left, HandSide.Right]
        actuation_points = [ActuationPoint.Thumb, ActuationPoint.Index, ActuationPoint.Middle, ActuationPoint.Annular, ActuationPoint.Pinky, ActuationPoint.Palm]
        for hs in hand_sides:
            if hs & self.handSideFlag:
                for ap in actuation_points:
                    if ap & self.actuationPointFlag:
                        msg.setHandSide(hs)
                        msg.setActuationPoint(ap)
                        self.__client._sendMessage(msg)

__all__ = ['WeArtHapticObject']
