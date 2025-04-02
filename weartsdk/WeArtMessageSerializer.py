from . import WeArtMessages as WeArtMessages
import json

class WeArtMessageSerializer:
    separator = ':'
    
    __MESSAGE_CLASSES = {
        WeArtMessages.StartFromClientMessage.ID:    WeArtMessages.StartFromClientMessage,
        WeArtMessages.TrackingMessage.ID:           WeArtMessages.TrackingMessage,
        WeArtMessages.TrackingBendingG2Message.ID:  WeArtMessages.TrackingBendingG2Message,
        WeArtMessages.StopFromClientMessage.ID:     WeArtMessages.StopFromClientMessage,
        WeArtMessages.CalibrationResultMessage.ID:  WeArtMessages.CalibrationResultMessage,
        WeArtMessages.CalibrationStatusMessage.ID:  WeArtMessages.CalibrationStatusMessage,
        WeArtMessages.SetTemperatureMessage.ID:     WeArtMessages.SetTemperatureMessage,
        WeArtMessages.StopTemperatureMessage.ID:    WeArtMessages.StopTemperatureMessage,
        WeArtMessages.SetForceMessage.ID:           WeArtMessages.SetForceMessage,
        WeArtMessages.StopForceMessage.ID:          WeArtMessages.StopForceMessage,
        WeArtMessages.SetTextureMessage.ID:         WeArtMessages.SetTextureMessage,
        WeArtMessages.StopTextureMessage.ID:        WeArtMessages.StopTextureMessage,
        WeArtMessages.RawSensorsData.ID:            WeArtMessages.RawSensorsData,
        WeArtMessages.RawDataTDPro.ID:              WeArtMessages.RawDataTDPro,
        WeArtMessages.GetMiddlewareStatus.ID:       WeArtMessages.GetMiddlewareStatus,
        WeArtMessages.MiddlewareStatusMessage.ID:   WeArtMessages.MiddlewareStatusMessage,
        WeArtMessages.WeArtAppStatusMessage.ID:     WeArtMessages.WeArtAppStatusMessage,
        WeArtMessages.GetDevicesStatusMessage.ID:   WeArtMessages.GetDevicesStatusMessage,
        WeArtMessages.DevicesStatusMessage.ID:      WeArtMessages.DevicesStatusMessage,
        WeArtMessages.TDProStatusMessage.ID:        WeArtMessages.TDProStatusMessage,
        WeArtMessages.AnalogSensorsData.ID:         WeArtMessages.AnalogSensorsData,
    }
        
    @staticmethod
    def __createMessage(id: str):
        message_class = WeArtMessageSerializer.__MESSAGE_CLASSES.get(id)
        if message_class:
            return message_class()
        else:
            return None

    def Deserialize(self, data: str) -> WeArtMessages.WeArtMessage:
        id = self.__extractID(data)
        msg = self.__createMessage(id)
        if msg != None:
            msg.deserialize(data)
        return msg

    def __extractID(self, data:str) -> str:
        try:
            # if it is a JSON message
            d = json.loads(data)
            return d["type"]
        except:
            # if it is a CSV message
            return data.split(":")[0]