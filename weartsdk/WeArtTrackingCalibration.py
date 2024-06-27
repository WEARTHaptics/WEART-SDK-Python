from .WeArtMessageListener import WeArtMessageListener
from .WeArtMessages import CalibrationResultMessage, CalibrationStatusMessage, WeArtMessage

class WeArtTrackingCalibration(WeArtMessageListener):
    def __init__(self):
        super().__init__([CalibrationStatusMessage.ID, CalibrationResultMessage.ID])
        self.__currentHand = None
        self.__status = None
        self.__result = False
        self.__statusCallbacks = []
        self.__resultCallbacks = []

    def getCurrentHand(self):
        return self.__currentHand
    
    def getStatus(self):
        return self.__status
    
    def getResult(self):
        return self.__result
    
    def AddStatusCallback(self, callback):
        self.__statusCallbacks.append(callback)
    
    def AddResultCallback(self, callback):
        self.__resultCallbacks.append(callback)
    
    def OnMessageReceived(self, message:WeArtMessage):
        if message.getID() == CalibrationStatusMessage.ID:
            self.__currentHand = message.getHand()
            self.__status = message.getStatus()
            for callback in self.__statusCallbacks:
                callback(self.__currentHand, self.__status)
        elif message.getID() == CalibrationResultMessage.ID:
            self.__currentHand = message.getHand()
            self.__result = message.getSuccess()
            for callback in self.__resultCallbacks:
                callback(self.__currentHand, self.__result)

__all__ = ['WeArtTrackingCalibration']
