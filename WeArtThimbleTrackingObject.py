from WeArtMessageListener import WeArtMessageListener
from WeArtMessage import WeArtMessage
from WeArtCommon import HandSide, ActuationPoint
from WeArtMessage import WeArtMessage
import WeArtCommon


class WeArtThimbleTrackingObject(WeArtMessageListener):
    def __init__(self, handSide:HandSide, actuationPoint:ActuationPoint):
        self._handSide = handSide
        self._actuation_point = actuationPoint
        self._closure = WeArtCommon.defaultClosure
        self._abduction = WeArtCommon.defaultAbduction
    
    def OnMessageReceived(self, message: WeArtMessage):
        return
    
    def GetClosure(self):
        return self._closure
    
    def GetAbduction(self):
        return self._abduction