from .WeArtMessageListener import WeArtMessageListener
from .WeArtCommon import HandSide, ActuationPoint
from .WeArtMessages import WeArtMessage, TrackingMessage
from . import WeArtCommon


class WeArtThimbleTrackingObject(WeArtMessageListener):
    def __init__(self, handSide:HandSide, actuationPoint:ActuationPoint):
        super().__init__([TrackingMessage.ID])
        self._handSide = handSide
        self._actuation_point = actuationPoint
        self._closure = WeArtCommon.defaultClosure
        self._abduction = WeArtCommon.defaultAbduction
    
    def OnMessageReceived(self, message: WeArtMessage):
        if message.getID() == TrackingMessage.ID:
            # it means that message is actually a TrackingMessage
            self._closure = message.GetClosure(self._handSide, self._actuation_point)
            self._abduction = message.GetAbduction(self._handSide, self._actuation_point)

    def GetClosure(self):
        return self._closure
    
    def GetAbduction(self):
        return self._abduction

__all__ = ['WeArtThimbleTrackingObject']
