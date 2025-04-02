from .WeArtMessageListener import WeArtMessageListener
from .WeArtCommon import HandSide, ActuationPoint, AnalogSensorRawData
from .WeArtMessages import WeArtMessage, AnalogSensorsData
from dataclasses import dataclass


@dataclass
class Sample:
    """
    Represents a sample of analog sensor data.

    Attributes:
        timestamp (int): The timestamp of the sample.
        data (AnalogSensorRawData): The raw data from the analog sensor.
    """
    timestamp: int = 0
    data: AnalogSensorRawData = None

class WeArtAnalogSensorData(WeArtMessageListener):
    """
    Listener for analog sensor data updates.

    This class listens for messages containing analog sensor data and notifies registered callbacks
    when a new sample of data is received. It filters the messages based on the specified hand side
    and actuation point.

    Inherits from:
        WeArtMessageListener: Base class for handling incoming messages.

    Attributes:
        __lastSample (Sample): Stores the last received sample of analog sensor data.
        __callbacks (list): List of registered callback functions to notify upon receiving new data.
        __handSide (HandSide): The hand side (left or right) to filter the sensor data.
        __actuationPoint (ActuationPoint): The actuation point to filter the sensor data.
    """
    def __init__(self, handSide: HandSide, actuationPoint: ActuationPoint):
        """
        Initializes the WeArtAnalogSensorData listener.

        Args:
            handSide (HandSide): Specifies the hand side (left or right) to filter the sensor data.
            actuationPoint (ActuationPoint): Specifies the actuation point to filter the sensor data.
        """
        super().__init__([AnalogSensorsData.ID])
        self.__lastSample = Sample()
        self.__callbacks = []
        self.__handSide = handSide
        self.__actuationPoint = actuationPoint

    def GetLastSample(self) -> Sample:
        """
        Retrieves the last received analog sensor data sample.

        Returns:
            Sample: The most recent analog sensor data sample.
        """
        return self.__lastSample
    
    def AddSampleCallback(self, callback):
        """
        Registers a callback function to be notified of new analog sensor data samples.

        The callback function should have the following signature:
            def callback(sample: Sample)

        Args:
            callback (Callable[[Sample], None]): Function to be called with the latest Sample.
        """
        self.__callbacks.append(callback)
    
    def OnMessageReceived(self, message: WeArtMessage):
        """
        Handles received analog sensor data messages.

        Filters the message based on hand side and actuation point. If valid, updates the last sample
        and calls registered callbacks with the new data.

        Args:
            message (WeArtMessage): The received message containing analog sensor data.
        """
        if message.getID() != AnalogSensorsData.ID:
            return 
        rawSensorsData = message
        if rawSensorsData == None:
            return
        if rawSensorsData.getHand() != self.__handSide:
            return
        if not rawSensorsData.hasSensor(self.__actuationPoint):
            return
        
        sample = Sample(timestamp = rawSensorsData.timestamp(), data = rawSensorsData.getSensor(self.__actuationPoint))
        self.__lastSample = sample
        for callback in self.__callbacks:
            callback(sample)

__all__ = ['WeArtAnalogSensorData']