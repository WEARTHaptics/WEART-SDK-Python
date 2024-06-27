from .WeArtMessageListener import WeArtMessageListener
from .WeArtCommon import HandSide, ActuationPoint, SensorData
from .WeArtMessages import WeArtMessage, RawSensorsData

from dataclasses import dataclass

@dataclass
class Sample:
    timestamp: int
    data: SensorData

class WeArtTrackingRawData(WeArtMessageListener):
    def __init__(self, handSide:HandSide, actuationPoint:ActuationPoint):
        super().__init__(RawSensorsData.ID)
        self.__handSide = handSide
        self.__actuationPoint = actuationPoint
        self.__K_NUM_SAMPLES = 3
        self.__samples = [] #std::queue<Sample> samples;
        self.__callbacks =  [] #std::vector<std::function<void(Sample)>> callbacks;

    def GetLastSample(self) -> Sample:
        if len(self.__samples) == 0:
            return Sample(0, SensorData(0, 0, 0))
        return self.__samples[-1]

    def AddSampleCallback(self, callback):
        self.__callbacks.append(callback)
    
    def OnMessageReceived(self, message: WeArtMessage):
        if message.getID() != RawSensorsData.ID: #to be checked
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
