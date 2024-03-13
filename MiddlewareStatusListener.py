from dataclasses import dataclass
from WeArtCommon import MiddlewareStatus, ConnectedDeviceStatus
from WeArtMessageListener import WeArtMessageListener
from WeArtMessages import MiddlewareStatusMessage, DevicesStatusMessage
from pySDK.WeArtMessages import WeArtMessage

@dataclass 
class MiddlewareStatusUpdate:
    timestamp: int
    status: MiddlewareStatus
    version: str
    statusCode: int
    errorDesc: str
    actuationsEnabled:bool
    devices: list[ConnectedDeviceStatus]

class MiddlewareStatusListener(WeArtMessageListener):
    def __init__(self):
        super().__init__(MiddlewareStatusMessage.ID, DevicesStatusMessage.ID)
        self.__statusCallbacks = []
        self.__data = MiddlewareStatusUpdate()
    
    def OnMessageReceived(self, message: WeArtMessage):
        toUpdate = False
        if message.getID() == MiddlewareStatusMessage.ID:
            mwStatus = message
            if mwStatus != None:
                newStatus = mwStatus.data()
                self.__data.timestamp = mwStatus.timestamp()
                self.__data.status = newStatus.status
                self.__data.version = newStatus.version
                self.__data.statusCode = newStatus.statusCode
                self.__data.errorDesc = newStatus.errorDesc
                self.__data.actuationsEnabled = newStatus.actuationsEnabled
                toUpdate = True
                
        elif message.getID() == DevicesStatusMessage.ID:
            deviceStatus = message
            if deviceStatus!= None:
                self.__data.timestamp = deviceStatus.timestamp()
                self.__data.devices = deviceStatus.devices()
                toUpdate = True

        if toUpdate:
            for callback in self.__statusCallbacks:
                callback(self.__data)
                

    def AddStatusCallback(self, callback):
        self.__statusCallbacks.append(callback)
    
    def lastStatus(self) -> MiddlewareStatusUpdate:
        return self.__data

    

