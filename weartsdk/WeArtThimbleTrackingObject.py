from .WeArtMessageListener import WeArtMessageListener
from .WeArtCommon import HandSide, ActuationPoint
from .WeArtMessages import WeArtMessage, TrackingMessage, TrackingBendingG2Message
from . import WeArtCommon

class WeArtThimbleTrackingObject(WeArtMessageListener):
    """
    Represents a tracking object for a WeArt thimble, which listens for messages regarding tracking and bending data.
    
    Attributes:
        _handSide (HandSide): The side of the hand (left or right) associated with the object.
        _actuation_point (ActuationPoint): The actuation point of the thimble (e.g., thumb, index).
        _closure (float): The closure value of the thimble, representing the relative closure of the thimble (0-1).
        _abduction (float): The abduction value of the thimble, representing the relative abduction of the thimble (0-1).

    Methods:
        OnMessageReceived: Handles the received message and updates the closure and abduction values accordingly.
        GetClosure: Returns the current closure value.
        GetAbduction: Returns the current abduction value.
    """
    def __init__(self, handSide: HandSide, actuationPoint: ActuationPoint):
        """
        Initializes the WeArtThimbleTrackingObject, setting the initial hand side, actuation point, 
        closure, and abduction values.

        Parameters:
            handSide (HandSide): The side of the hand (left or right).
            actuationPoint (ActuationPoint): The actuation point (e.g., thumb, index).
        """
        super().__init__([TrackingMessage.ID, TrackingBendingG2Message.ID])
        self._handSide = handSide
        self._actuation_point = actuationPoint
        self._closure = WeArtCommon.defaultClosure
        self._abduction = WeArtCommon.defaultAbduction
    
    def OnMessageReceived(self, message: WeArtMessage):
        """
        Handles the received tracking or bending message, updating the closure and abduction values.

        Parameters:
            message (WeArtMessage): The message containing tracking or bending data.
        """
        if message.getID() == TrackingMessage.ID:
            self._closure = message.GetClosure(self._handSide, self._actuation_point)
            self._abduction = message.GetAbduction(self._handSide, self._actuation_point)
        elif message.getID() == TrackingBendingG2Message.ID and self._handSide == message.GetHandSide():
            self._closure = message.GetClosure(self._actuation_point)
            self._abduction = message.GetAbduction(self._actuation_point)

    def GetClosure(self):
        """
        Returns the current closure value. 0 means fully open, 1 means fully closed.
        This value is available for all thimbles.

        Returns:
            float: The relative closure value of finger (0-1).
        """
        return self._closure
    
    def GetAbduction(self):
        """
        Returns the current abduction value. 0 means fully adducted, 1 means fully abducted.
        """
        return self._abduction

__all__ = ['WeArtThimbleTrackingObject']
