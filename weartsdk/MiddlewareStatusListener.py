from dataclasses import dataclass, field
from typing import List
from .WeArtCommon import MiddlewareStatus, MiddlewareConnectedDevice
from .WeArtMessageListener import WeArtMessageListener
from .WeArtMessages import MiddlewareStatusMessage, WeArtAppStatusMessage, DevicesStatusMessage
from .WeArtMessages import WeArtMessage
import logging

@dataclass 
class MiddlewareStatusUpdate:
    """
    Represents an update of the middleware status.

    Attributes:
        timestamp (int): The timestamp of the status update.
        status (MiddlewareStatus): The current status of the middleware.
        version (str): The version of the middleware.
        statusCode (int): The status code representing middleware state.
        errorDesc (str): A description of any error that occurred.
        warningCode (int): The warning code representing WeArtApp warning state (TD Pro only).
        warningDesc (str): A description of any warning that occurred (TD Pro only).
        actuationsEnabled (bool): Indicates if actuation is enabled.
        connectionType (str): The type of connection used (TD Pro only).
        autoconnection (bool): Indicates if autoconnection is enabled (TD Pro only).
        trackingPlayback (bool): Indicates if tracking playback is active (TD Pro only).
        rawDataLog (bool): Indicates if raw data logging is active (TD Pro only).
        sensorOnMask (bool): Indicates if sensors are enabled (TD Pro only).
        connectedDevices (List[MiddlewareConnectedDevice]): List of connected devices.
    """
    timestamp: int = 0
    status: MiddlewareStatus = MiddlewareStatus(0)
    version: str = ""
    statusCode: int = 0
    errorDesc: str = ""
    warningCode: int = 0                # G2 ONLY
    warningDesc: str = ""               # G2 ONLY
    actuationsEnabled:bool = False
    connectionType: str = "NONE"        # G2 ONLY
    autoconnection: bool = False        # G2 ONLY
    trackingPlayback: bool = False      # G2 ONLY                               
    rawDataLog: bool = False            # G2 ONLY
    sensorOnMask: bool = False          # G2 ONLY
    connectedDevices: List[MiddlewareConnectedDevice] = field(default_factory=list)

class MiddlewareStatusListener(WeArtMessageListener):
    """
    Listener for Middleware status updates.

    This class listens for messages regarding the Middleware and WeArtApp status 
    and notifies registered callbacks when a new status update is received.

    Inherits from:
        WeArtMessageListener: Base class for handling incoming messages.

    Attributes:
        __statusCallbacks (list): List of registered status update callbacks.
        __data (MiddlewareStatusUpdate): Stores the latest middleware status update.
        __logger (logging.Logger): Logger instance for debugging and status tracking.
    """
    def __init__(self):
        super().__init__([MiddlewareStatusMessage.ID, WeArtAppStatusMessage.ID, DevicesStatusMessage.ID])
        self.__statusCallbacks = []
        self.__data = MiddlewareStatusUpdate()
        self.__logger = logging.getLogger("WeArtClient")
    
    def OnMessageReceived(self, message: WeArtMessage):
        """
        Handles received Middleware and WeArtStatus.

        Extracts relevant data from the message and updates the stored status. Calls registered callbacks with the new data.

        Args:
            message (WeArtMessage): The received status message.
        """
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
            self.__data.connectedDevices = newStatus.connectedDevices
            self.__logger.debug(self.__data)
            toUpdate = True
        
        elif message.getID() == WeArtAppStatusMessage.ID:
            waStatus = message
            newStatus = waStatus.data()
            self.__data.timestamp = waStatus.timestamp()
            self.__data.status = newStatus.status
            self.__data.version = newStatus.version
            self.__data.statusCode = newStatus.statusCode
            self.__data.errorDesc = newStatus.errorDesc
            self.__data.warningCode = newStatus.warningCode
            self.__data.warningDesc = newStatus.warningDesc
            self.__data.actuationsEnabled = newStatus.actuationsEnabled
            self.__data.connectionType = newStatus.connectionType
            self.__data.autoconnection = newStatus.autoconnection
            self.__data.trackingPlayback = newStatus.trackingPlayback
            self.__data.rawDataLog = newStatus.rawDataLog
            self.__data.sensorOnMask = newStatus.sensorOnMask
            self.__data.connectedDevices = newStatus.connectedDevices
            self.__logger.debug(self.__data)
            toUpdate = True

        if toUpdate:
            for callback in self.__statusCallbacks:
                callback(self.__data)
                
    def AddStatusCallback(self, callback):
        """
        Registers a callback function to be notified of middleware status updates.
        The callback has the following signature:\n
            def callback(status: MiddlewareStatusUpdate)

        Args:
            callback (Callable[[MiddlewareStatusUpdate], None]): Function to be called 
                with the latest MiddlewareStatusUpdate.
        """
        self.__statusCallbacks.append(callback)
    
    def LastStatus(self) -> MiddlewareStatusUpdate:
        """
        Retrieves the last received middleware status update.

        Returns:
            MiddlewareStatusUpdate: The most recent middleware status update.
        """
        return self.__data

__all__ = ['MiddlewareStatusListener', 'MiddlewareStatusUpdate']