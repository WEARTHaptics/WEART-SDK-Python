from WeArtMessageListener import WeArtMessageListener
from WeArtCommon import HandSide, ActuationPoint, AnalogSensorRawData
from WeArtMessages import WeArtMessage, AnalogSensorsData
from dataclasses import dataclass


@dataclass
class Sample:
    timestamp: int
    data: AnalogSensorRawData

class WeArtAnalogSensorData(WeArtMessageListener):

    def __init__(self, handSide:HandSide, actuationPoint:ActuationPoint):
        super().__init__([AnalogSensorsData.ID])
        self.__lastSample = None #Sample lastSample;
        self.__callbacks = [] #std::vector<std::function<void(Sample)>> callbacks;
        self.__handSide = handSide
        self.__actuationPoint = actuationPoint


    def GetLastSample(self) -> Sample:
        return self.__lastSample
    
    def AddSampleCallback(self, callback):
        self.__callbacks.append(callback)
    
    def OnMessageReceived(self, message: WeArtMessage):
        if message.getID() != AnalogSensorsData.ID: #to be checked
            return 
        rawSensorsData = message # cast to AnalogSensorsData
        if rawSensorsData == None:
            return
        if rawSensorsData.getHand() != self.__handSide:
            return
        if not rawSensorsData.hasSensor(self.__actuationPoint):
            return
        
        sample = Sample(timestamp = rawSensorsData.timestamp(), data = rawSensorsData.getSensors(self.__actuationPoint))
        self.__lasample = sample
        for callback in self.__callbacks:
            callback(sample)
