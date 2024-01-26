import WeArtMessages as WeArtMessages

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
        
    @staticmethod
    def createMessage(id:str):
        h = WeArtMessageSerializer.HashStringToInt(id)
        if (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.StartFromClientMessage.ID)):
            return WeArtMessages.StartFromClientMessage()
        elif (h == WeArtMessageSerializer.HashStringToInt(WeArtMessages.TrackingMessage.ID)):
            return WeArtMessages.TrackingMessage()
        #TODO Continues...
        else: 
            return None
        '''   
            case HashStringToInt(StopFromClientMessage::ID): return new StopFromClientMessage();
            case HashStringToInt(CalibrationResultMessage::ID): return new CalibrationResultMessage();
            case HashStringToInt(CalibrationStatusMessage::ID): return new CalibrationStatusMessage();
            case HashStringToInt(ExitMessage::ID): return new ExitMessage();
            case HashStringToInt(DisconnectMessage::ID): return new DisconnectMessage();
            case HashStringToInt(SetTemperatureMessage::ID): return new SetTemperatureMessage();
            case HashStringToInt(StopTemperatureMessage::ID): return new StopTemperatureMessage();
            case HashStringToInt(SetForceMessage::ID): return new SetForceMessage();
            case HashStringToInt(StopForceMessage::ID): return new StopForceMessage();
            case HashStringToInt(SetTextureMessage::ID): return new SetTextureMessage();
            case HashStringToInt(StopTextureMessage::ID): return new StopTextureMessage();
        '''

    # @brief Serializes the given message to a string (ready to send on the network connection)
	# @param message Message to serialize
	# @return the serialized message as string
	#std::string Serialize(WeArtMessage* message);
    @staticmethod
    def Serialize(message:WeArtMessages.WeArtMessage):
        messageID = message.getID()
        serializedValues = message.getValues()
        serializedValues.insert(0, messageID)

        res = serializedValues[0]
        for i in range(1, len(serializedValues)):
            res += WeArtMessageSerializer.separator
            res += serializedValues[i]
        
        return res


	# @brief Serializes a strirng into a bytestream
	# @param text The string to serialize
	# @return the serialized string
	#uint8* Serialize(std::string text);

    #TODO: maybe to be implemented

	# @brief Deserializes a string into the corresponding message object
	# @param data String containing the serialized message
	# @return the message deserialized from the given string
	#WeArtMessage* Deserialize(std::string data);
    @staticmethod
    def Deserialize(data:str):
        strings = data.split(WeArtMessageSerializer.separator)
        messageID = strings[0]
        msg = WeArtMessageSerializer.createMessage(messageID)

        if msg:
            msg.setValues(strings[1:])
        
        return msg

	# Bytestream to std::string.

	# @brief Converts a bytestream to string
	# @param byteData Pointer to the data buffer to convert
	# @param byteCount Size of the data buffer to convert
	# @return deserializes buffer as string
	#std::string Deserialize(uint8* byteData, int byteCount);

    #TODO: maybe to be implemented
