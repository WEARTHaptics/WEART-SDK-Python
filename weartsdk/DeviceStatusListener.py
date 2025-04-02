from dataclasses import dataclass, field
from typing import List
from .WeArtCommon import ConnectedDeviceStatus
from .WeArtMessageListener import WeArtMessageListener
from .WeArtMessages import DevicesStatusMessage
from .WeArtMessages import WeArtMessage
import logging

@dataclass 
class DeviceStatusUpdate:
    """
    Represents an update of the device status.

    Attributes:
        timestamp (int): The timestamp of the status update.
        devices (List[ConnectedDeviceStatus]): A list of connected device statuses.
    """
    timestamp: int = 0
    devices: List[ConnectedDeviceStatus] = field(default_factory=list)

class DeviceStatusListener(WeArtMessageListener):
    """
    Listener for device status updates.

    This class listens for device status messages and notifies registered callbacks 
    when a new status update is received.

    Inherits from:
        WeArtMessageListener: Base class for handling incoming messages.

    Attributes:
        __statusCallbacks (list): List of registered status update callbacks.
        __data (DeviceStatusUpdate): Stores the latest device status update.
        __logger (logging.Logger): Logger instance for debugging and status tracking.
    """
    def __init__(self):
        super().__init__([DevicesStatusMessage.ID])
        self.__statusCallbacks = []
        self.__data = DeviceStatusUpdate()
        self.__logger = logging.getLogger("WeArtClient")
    
    def OnMessageReceived(self, message: WeArtMessage):
        """
        Handles received device status messages.

        Extracts timestamp and device status information from the message and 
        updates the stored status. Calls registered callbacks with the new data.

        Args:
            message (WeArtMessage): The received device status message.
        """
        devStatus = message
        self.__data.timestamp = devStatus.timestamp()
        self.__data.devices = devStatus.devices()
        self.__logger.debug(self.__data)
        
        for callback in self.__statusCallbacks:
            callback(self.__data)                

    def AddStatusCallback(self, callback):
        """
        Registers a callback function to be notified of device status updates.
        The callback has the following signature:\n
            def callback(status: DeviceStatusUpdate)

        Args:
            callback (Callable[[DeviceStatusUpdate], None]): Function to be called 
            with the latest DeviceStatusUpdate.
        """
        self.__statusCallbacks.append(callback)
    
    def LastStatus(self) -> DeviceStatusUpdate:
        """
        Retrieves the last received device status update.

        Returns:
            DeviceStatusUpdate: The most recent device status update.
        """
        return self.__data

__all__ = ['DeviceStatusListener', 'DeviceStatusUpdate']