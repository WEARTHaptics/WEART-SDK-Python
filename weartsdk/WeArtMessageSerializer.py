from . import WeArtMessages as WeArtMessages
import json

class WeArtMessageSerializer:
    separator = ':'
    
    @staticmethod
    def HashStringToInt(string:str, _hash = 0):
        return WeArtMessageSerializer._hashstringtoint(string, 0, _hash)
    
    @staticmethod
    def _hashstringtoint(string:str, index:int, _hash = 0):
        if (index == len(string)):
            return _hash
        else:
            return 101 * WeArtMessageSerializer._hashstringtoint(string, index+1, _hash) + ord(string[index])


	# @brief Creates a message of the right type given its type ID
	# @param ID Type of the message to create
	# @return the created message
        
    def __createMessage(self, id:str):
        h = WeArtMessageSerializer.HashStringToInt(id)
        if (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.StartFromClientMessage.ID)):
            return WeArtMessages.StartFromClientMessage()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.TrackingMessage.ID)):
            return WeArtMessages.TrackingMessage()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.StopFromClientMessage.ID)):
            return WeArtMessages.StopFromClientMessage()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.CalibrationResultMessage.ID)):
            return WeArtMessages.CalibrationResultMessage()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.CalibrationStatusMessage.ID)):
            return WeArtMessages.CalibrationStatusMessage()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.SetTemperatureMessage.ID)):
            return WeArtMessages.SetTemperatureMessage()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.StopTemperatureMessage.ID)):
            return WeArtMessages.StopTemperatureMessage()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.SetForceMessage.ID)):
            return WeArtMessages.SetForceMessage()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.StopForceMessage.ID)):
            return WeArtMessages.StopForceMessage()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.SetTextureMessage.ID)):
            return WeArtMessages.SetTextureMessage()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.StopTextureMessage.ID)):
            return WeArtMessages.StopTextureMessage()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.RawSensorsData.ID)):
            return WeArtMessages.RawSensorsData()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.GetMiddlewareStatus.ID)):
            return WeArtMessages.GetMiddlewareStatus()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.MiddlewareStatusMessage.ID)):
            return WeArtMessages.MiddlewareStatusMessage()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.GetDevicesStatusMessage.ID)):
            return WeArtMessages.GetDevicesStatusMessage()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.DevicesStatusMessage.ID)):
            return WeArtMessages.DevicesStatusMessage()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.AnalogSensorsData.ID)):
            return WeArtMessages.AnalogSensorsData()
        #TODO Continues...
        else: 
            return None
        '''   
            case HashStringToInt(ExitMessage::ID): return new ExitMessage();
            case HashStringToInt(DisconnectMessage::ID): return new DisconnectMessage();
        '''

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

	# Bytestream to std::string.

	# @brief Converts a bytestream to string
	# @param byteData Pointer to the data buffer to convert
	# @param byteCount Size of the data buffer to convert
	# @return deserializes buffer as string
	#std::string Deserialize(uint8* byteData, int byteCount);

    #TODO: maybe to be implemented
