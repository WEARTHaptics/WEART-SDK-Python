from .WeArtMessageListener import WeArtMessageListener
from .WeArtCommon import HandSide, ActuationPoint, SensorData, AccelerometerData, GyroscopeData, TofData
from .WeArtMessages import WeArtMessage, RawSensorsData, RawDataTDPro
from dataclasses import dataclass

@dataclass
class Sample:
    """
    Represents a sample of raw sensor data.

    Attributes:
        timestamp (int): The timestamp of the sample.
        data (SensorData): The sensor data associated with the sample.
    """
    timestamp: int
    data: SensorData

class WeArtTrackingRawData(WeArtMessageListener):
    """
    Handles raw tracking data from WeArt sensors, processing sensor data messages 
    and notifying registered callbacks when new data is available.

    Attributes:
        __handSide (HandSide): The hand side (left or right) associated with the data.
        __actuationPoint (ActuationPoint): The specific actuation point being tracked.
        __K_NUM_SAMPLES (int): The maximum number of stored samples.
        __samples (list): A list of stored sensor data samples.
        __callbacks (list): A list of callback functions to be executed when a new sample is received.

    Methods:
        GetLastSample: Returns the most recent sensor data sample.
        AddSampleCallback: Registers a callback function to be called when new sensor data arrives.
        OnMessageReceived: Processes incoming messages and updates the stored samples.
    """
    def __init__(self, handSide: HandSide, actuationPoint: ActuationPoint):
        """
        Initializes the tracking object to listen for raw sensor data messages.

        Parameters:
            handSide (HandSide): The hand side (left or right) to track.
            actuationPoint (ActuationPoint): The specific actuation point to track.
        """
        super().__init__([RawSensorsData.ID, RawDataTDPro.ID])
        self.__handSide = handSide
        self.__actuationPoint = actuationPoint
        self.__K_NUM_SAMPLES = 3
        self.__samples = []
        self.__callbacks =  []

    def GetLastSample(self) -> Sample:
        """
        Returns the most recent sensor data sample, or a default sample with timestamp = 0 if no data is available.

        Returns:
            Sample: The last recorded sample.
        """
        if len(self.__samples) == 0:
            return Sample(0, SensorData(AccelerometerData(), GyroscopeData(), TofData()))
        return self.__samples[-1]

    def AddSampleCallback(self, callback):
        """
        Registers a callback function to be called when new sensor data arrives.
        The callback function should accept a Sample object as an argument.
        The callback signature should match the following:\n
            def callback(sample: Sample)

        Parameters:
            callback (function): A function that receives a Sample object as an argument.
        """
        self.__callbacks.append(callback)
    
    def OnMessageReceived(self, message: WeArtMessage):
        """
        Processes incoming messages, extracts relevant sensor data, and updates the stored samples.

        If the message does not contain relevant data for the configured hand side or actuation point, 
        it is ignored. When valid data is received, it is stored in the sample list and the registered 
        callbacks are notified.

        Parameters:
            message (WeArtMessage): The received message containing sensor data.
        """
        if message.getID() != RawSensorsData.ID and message.getID() != RawDataTDPro.ID:
            return
        rawSensorsData = message
        if rawSensorsData == None:
            return
        if rawSensorsData.getHand() != self.__handSide:
            return
        if not rawSensorsData.hasSensor(self.__actuationPoint):
            return 

        sample = Sample(timestamp = rawSensorsData.timestamp(), data = rawSensorsData.getSensor(self.__actuationPoint))
        self.__samples.append(sample)

        while len(self.__samples) > self.__K_NUM_SAMPLES:
            self.__samples.pop(0)
        
        for callback in self.__callbacks:
            callback(sample)

__all__ = ['WeArtTrackingRawData']
