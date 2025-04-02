from dataclasses import dataclass, field
from typing import List
from .WeArtCommon import G2DeviceStatus
from .WeArtMessageListener import WeArtMessageListener
from .WeArtMessages import TDProStatusMessage
from .WeArtMessages import WeArtMessage
import logging

@dataclass 
class TDProStatusUpdate:
    """
    Represents an update of the Touch Diver Pro device status.

    Attributes:
        timestamp (int): The timestamp of the status update.
        devices (List[G2DeviceStatus]): List of connected Touch Diver Pro devices and their status.
    """
    timestamp: int = 0
    devices: List[G2DeviceStatus] = field(default_factory=list)

class TDProStatusListener(WeArtMessageListener):
    """
    Listener for Touch Diver Pro device status updates.

    This class listens for status messages from Touch Diver Pro devices and notifies
    registered callbacks when a new status update is received.

    Inherits from:
        WeArtMessageListener: Base class for handling incoming messages.

    Attributes:
        __statusCallbacks (list): List of registered status update callbacks.
        __data (TDProStatusUpdate): Stores the latest TouchDiver Pro device status update.
        __logger (logging.Logger): Logger instance for debugging and status tracking.
    """
    def __init__(self):
        super().__init__([TDProStatusMessage.ID])
        self.__statusCallbacks = []
        self.__data = TDProStatusUpdate()
        self.__logger = logging.getLogger("WeArtClient")
    
    def OnMessageReceived(self, message: WeArtMessage):
        """
        Handles received Touch Diver Pro status messages.

        Extracts relevant data from the message and updates the stored status.
        Calls registered callbacks with the new data.

        Args:
            message (WeArtMessage): The received Touch Diver Pro status message.
        """
        TDProStatus = message
        self.__data.timestamp = TDProStatus.timestamp()
        self.__data.devices = TDProStatus.devices()

        for callback in self.__statusCallbacks:
            callback(self.__data)                

    def AddStatusCallback(self, callback):
        """
        Registers a callback function to be notified of Touch Diver Pro status updates.
        The callback has the following signature:\n
            def callback(status: TDProStatusUpdate)

        Args:
            callback (Callable[[TDProStatusUpdate], None]): Function to be called 
                with the latest TDProStatusUpdate.
        """
        self.__statusCallbacks.append(callback)
    
    def LastStatus(self) -> TDProStatusUpdate:
        """
        Retrieves the last received Touch Diver Pro device status update.

        Returns:
            TDProStatusUpdate: The most recent Touch Diver Pro device status update.
        """
        return self.__data

__all__ = ['TDProStatusListener', 'TDProStatusUpdate']