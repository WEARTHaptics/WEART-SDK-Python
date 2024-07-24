from dataclasses import dataclass, field
from typing import List
from .WeArtCommon import MiddlewareStatus, ConnectedDeviceStatus
from .WeArtMessageListener import WeArtMessageListener
from .WeArtMessages import MiddlewareStatusMessage, DevicesStatusMessage
from .WeArtMessages import WeArtMessage
import logging

@dataclass 
class MiddlewareStatusUpdate:
    timestamp: int = 0
    status: MiddlewareStatus = MiddlewareStatus(0)
    version: str = ""
    statusCode: int = 0
    errorDesc: str = ""
    actuationsEnabled:bool = False
    devices: List = field(default_factory=lambda: [])

class MiddlewareStatusListener(WeArtMessageListener):
    def __init__(self):
        super().__init__([MiddlewareStatusMessage.ID, DevicesStatusMessage.ID])
        self.__statusCallbacks = []
        self.__data = MiddlewareStatusUpdate()
        self.__logger = logging.getLogger("WeArtClient")
    
    def OnMessageReceived(self, message: WeArtMessage):
        toUpdate = False
        if message.getID() == MiddlewareStatusMessage.ID:
            mwStatus = message
            newStatus = mwStatus.data()
            self.__data.timestamp = mwStatus.timestamp()
            self.__data.status = newStatus.status
            self.__data.version = newStatus.version
            self.__data.statusCode = newStatus.statusCode
            self.__data.errorDesc = newStatus.errorDesc
            self.__data.actuationsEnabled = newStatus.actuationsEnabled
            self.__logger.debug(self.__data)
            toUpdate = True

        elif message.getID() == DevicesStatusMessage.ID:
            deviceStatus = message
            if deviceStatus!= None:
                self.__data.timestamp = deviceStatus.timestamp()
                self.__data.devices = deviceStatus.devices()
                self.__logger.debug(self.__data)
                toUpdate = True

        if toUpdate:
            for callback in self.__statusCallbacks:
                callback(self.__data)
                

    def AddStatusCallback(self, callback):
        self.__statusCallbacks.append(callback)
    
    def lastStatus(self) -> MiddlewareStatusUpdate:
        return self.__data

__all__ = ['MiddlewareStatusListener', 'MiddlewareStatusUpdate']