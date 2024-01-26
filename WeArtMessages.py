from WeArtCommon import TrackingType, HandSide, ActuationPoint, CalibrationStatus
import WeArtCommon
from pySDK.WeArtCommon import HandSide

def StringToTrackingType(string:str):
	if (string == "TrackType1"):
		return TrackingType.WEART_HAND
	return TrackingType.DEFAULT

def TrackingTypeToString(trackType:TrackingType):
    if trackType == TrackingType.DEFAULT:
        return ""
    elif trackType == TrackingType.WEART_HAND:
        return "TrackType1"
    else:
	    return ""
    
def StringToHandside(string:str):
    if (string == "LEFT"):
        return HandSide.Left
    elif (string == "RIGHT"):
        return HandSide.Right
    else:
        assert(False)
        return HandSide.Left

def HandsideToString(hs:HandSide):
    if (hs == HandSide.Left):
        return "LEFT"
    elif (hs == HandSide.Right):
        return "RIGHT"
    else:
        assert(False)
        return ""


def StringToActuationPoint(string:str):
    if string == "THUMB":
        return ActuationPoint.Thumb
    elif string == "INDEX":
        return ActuationPoint.Index
    elif string == "MIDDLE":
        return ActuationPoint.Middle
    elif string == "PALM":
        return ActuationPoint.Palm
    else:
        assert(False)
        return ActuationPoint.Thumb


def ActuationPointToString(ap: ActuationPoint):
    if ap == ActuationPoint.Thumb:
        return "THUMB"
    elif ap == ActuationPoint.Index:
        return "INDEX"
    elif ap == ActuationPoint.Middle:
        return "MIDDLE"
    elif ap == ActuationPoint.Palm:
        return "PALM"
    else:
        assert(False)
        return ""
    
def CalibrationHandSideToString(hs: HandSide):
    return "0" if hs == HandSide.Left else "1"
    

def StringToCalibrationHandSide(string: str):
    if (string == "0"):
        return HandSide.Left
    elif (string == "1"):
        return HandSide.Right
    assert(False)
    return HandSide.Left


class WeArtMessage:
	#@brief Allows to get the message ID, used to deserialize the correct message type
	#@return the message ID
    def __init__(self):
        return

    def getID(self):
        return

    def getValues(self):
        return []

    def setValues(self):
        return

    def setHandSide(self, handside:HandSide):
        return

    def setActuationPoint(self, actuation_point:ActuationPoint):
        return



class WeArtMessageNoParams(WeArtMessage):
   
    # the message carries no value, so return empty list
    def getValues(self):
        return []
    # the message carries no value, so return without doint anything
    def setValues(self, values):
        return
    


class WeArtMessageObjectSpecific(WeArtMessage):
    def __init__(self):
        self._handSide = None
        self._actuationPoint = None
    
    def setHandSide(self, handside:HandSide):
        self._handSide = handside
    
    def getActuationPoint(self):
        return self._actuationPoint
    
    def setActuationPoint(self, actuation_point:ActuationPoint):
        self._actuationPoint = actuation_point


class WeArtMessageHandSpecific(WeArtMessage):
    def __init__(self):
        super().__init__()
        self._handSide = None

    def getHand(self):
        return self._handSide

    def setHandSide(self, handside: HandSide):
        self._handSide = handside
    
    def setActuationPoint(self, actuation_point: ActuationPoint):
        return


class StartFromClientMessage(WeArtMessageNoParams):
    ID = "StartFromClient"

    def __init__(self, trackType = TrackingType.WEART_HAND):
        self._tracktype = trackType

    def getID(self):
        return self.ID
    
    def getValues(self):
        res = []
        if self._tracktype != TrackingType.DEFAULT:
            res.append(WeArtCommon.WEART_SDK_TYPE)
            res.append(WeArtCommon.WEART_SDK_VERSION)
            res.append(TrackingTypeToString(self._tracktype))
        return res

    def setValues(self, values:list[str]):
        if (len(values) == 0):
            self._trackType = TrackingType.DEFAULT
        else:
            self._trackType = StringToTrackingType(values[2])
        return

class StopFromClientMessage(WeArtMessageNoParams):
    ID = "StopFromClient"

    def getID(self):
        return self.ID
    


class CalibrationStatusMessage(WeArtMessageHandSpecific):
    ID = "CalibrationStatus"

    def __init__(self):
        super().__init__()
        self._status = None

    def getID(self):
        return self.ID
    
    def getStatus(self):
        return self._status
    
    def getValues(self):
        ret = []
        ret.append(CalibrationHandSideToString(self._handSide))
        ret.append(str(int(self._status)))
        return ret

    def setValues(self, values:list[str]):
        assert(len(values) == 2)
        self._handSide = StringToCalibrationHandSide(values[0])
        self._status = CalibrationStatus(int(values[1]))
        print(self._status)



class CalibrationResultMessage(WeArtMessageHandSpecific):
    ID = "CalibrationResult"

    def __init__(self):
        super().__init__()
        self._success = False

    def getID(self):
        return self.ID
    
    def getSuccess(self):
        return self._success
    
    def getValues(self):
        ret = []
        ret.append(CalibrationHandSideToString(self._handSide))
        ret.append("0" if self._success else "1")
        return ret 

    def setValues(self, values: list[str]):
        assert(len(values) == 2)
        self._handSide = StringToCalibrationHandSide(values[0])
        self._success = int(values[1]) == 0


class TrackingMessage(WeArtMessageNoParams):
    ID = "Tracking"

    def __init__(self, trackType = TrackingType.WEART_HAND):
        self.Angles = {"X":0.0, "Y": 0.0, "Z": 0.0}
        self._trackingType = trackType
        # Closures
        self.__RightThumbClosure = 0
        self.__RightIndexClosure = 0
        self.__RightMiddleClosure = 0
        self.__RightPalmClosure = 0
        self.__LeftThumbClosure = 0
        self.__LeftIndexClosure = 0
        self.__LeftMiddleClosure = 0
        self.__LeftPalmClosure = 0

        # Abductions
        self.__RightThumbAbduction = 0
        self.__LeftThumbAbduction = 0

    def getID(self):
        return self.ID

    def getValues(self):
        ret = []
        ret.append(TrackingTypeToString(self._trackingType))
        if self._trackingType == TrackingType.DEFAULT:
            ret.append(str(self.__RightThumbClosure))
            ret.append(str(self.__RightIndexClosure))
            ret.append(str(self.__RightMiddleClosure))
            ret.append(str(self.__RightPalmClosure))
            ret.append(str(self.__LeftThumbClosure))
            ret.append(str(self.__LeftIndexClosure))
            ret.append(str(self.__LeftMiddleClosure))
            ret.append(str(self.__LeftPalmClosure))
        elif self._trackingType == TrackingType.WEART_HAND:
            ret.append(str(self.__RightIndexClosure))
            ret.append(str(self.__RightThumbClosure))
            ret.append(str(self.__RightThumbAbduction))
            ret.append(str(self.__RightMiddleClosure))
            
            ret.append(str(self.__LeftIndexClosure))
            ret.append(str(self.__LeftThumbClosure))
            ret.append(str(self.__LeftThumbAbduction))
            ret.append(str(self.__LeftMiddleClosure))
        return ret
    
    def SetValues(self, values:list[str]):
        self._trackingType = StringToTrackingType(values[0])
        if self._trackingType == TrackingType.DEFAULT:
            assert(len(values)==8)
            self.__RightThumbClosure = int(values[0])
            self.__RightIndexClosure = int(values[1])
            self.__RightMiddleClosure = int(values[2])
            self.__RightPalmClosure = int(values[3])
            self.__LeftThumbClosure = int(values[4])
            self.__LeftIndexClosure = int(values[5])
            self.__LeftMiddleClosure = int(values[6])
            self.__LeftPalmClosure = int(values[7])
        elif self._trackingType == TrackingType.WEART_HAND:
            self.__RightIndexClosure = int(values[0])
            self.__RightThumbClosure = int(values[1])
            self.__RightThumbAbduction = int(values[2])
            self.__RightMiddleClosure = int(values[3])

            self.__LeftIndexClosure = int(values[5])
            self.__LeftThumbClosure = int(values[6])
            self.__LeftThumbAbduction = int(values[7])
            self.__LeftMiddleClosure = int(values[8])

    def GetType(self):
        return self._trackingType
    
    def GetAbduction(self, handSide:HandSide, actuationPoint:ActuationPoint):
        maxAbductionValue = 255.0
        if handSide == HandSide.Left:
            if (actuationPoint == ActuationPoint.Thumb):
                return float(self.__LeftThumbAbduction) / maxAbductionValue
        elif handSide == HandSide.Right:
            if (actuationPoint == ActuationPoint.Thumb):
                return float(self.__RightThumbAbduction) / maxAbductionValue
        return WeArtCommon.defaultAbduction
    
    
    def GetClosure(self, handSide:HandSide, actuationPoint:ActuationPoint):
        byteValue = 0
        if handSide == HandSide.Left:
            if actuationPoint == ActuationPoint.Thumb:
                byteValue = self.__LeftThumbClosure
            elif actuationPoint == ActuationPoint.Index:
                byteValue = self.__LeftIndexClosure
            elif actuationPoint == ActuationPoint.Middle:
                byteValue = self.__LeftMiddleClosure
            elif actuationPoint == ActuationPoint.Palm:
                byteValue = self.__LeftPalmClosure
        elif handSide == HandSide.Right:
            if actuationPoint == ActuationPoint.Thumb:
                byteValue = self.__RightThumbClosure
            elif actuationPoint == ActuationPoint.Index:
                byteValue = self.__RightIndexClosure
            elif actuationPoint == ActuationPoint.Middle:
                byteValue = self.__RightMiddleClosure
            elif actuationPoint == ActuationPoint.Palm:
                byteValue = self.__RightPalmClosure
        closure = float(byteValue) / float(255)
        return closure
    
class SetTemperatureMessage(WeArtMessageObjectSpecific):
    ID = "temperature"

    def __init__(self, t:float):
        super().__init__()
        self._temperature = t
    
    def getID(self):
        return self.ID
    
    def getValues(self):
        ret = []
        ret.append(str(self._temperature))
        ret.append(HandsideToString(self._handSide))
        ret.append(ActuationPointToString(self._actuationPoint))
        return ret
    
    def setValues(self, values:list[str]):
        assert(len(values)==3)
        self._temperature = float(values[0])
        self._handSide = StringToHandside(values[1])
        self._actuationPoint= StringToActuationPoint(values[2])

    
class StopTemperatureMessage(WeArtMessageObjectSpecific):
    ID = "stopTemperature"

    def __init__(self):
        super().__init__()

    def getID(self):
        return self.ID
    

    def getValues(self):
        ret = [HandsideToString(self._handSide), ActuationPointToString(self._actuationPoint)]
        return ret
    
    def setValues(self, values: list[str]):
        assert(len(values) == 2)
        self._handSide = StringToHandside(values[0])
        self._actuationPoint = StringToActuationPoint(values[1])

class SetForceMessage(WeArtMessageObjectSpecific):
    ID = "force"

    def __init__(self, force:list[float]):
        super().__init__()
        self._force = force

    def getID(self):
        return self.ID
    
    def getValues(self):
        ret = []
        ret.append(str(self._force[0]))
        ret.append(str(self._force[1]))
        ret.append(str(self._force[2]))
        ret.append(HandsideToString(self._handSide))
        ret.append(ActuationPointToString(self._actuationPoint))
        return ret
    
    def setValues(self, values:list[str]):
        assert(len(values) == 5)
        self._force[0] = float(values[0])
        self._force[1] = float(values[1])
        self._force[2] = float(values[2])
        self._handSide = StringToHandside(values[3])
        self._actuationPoint = StringToActuationPoint(values[4])

class StopForceMessage(WeArtMessageObjectSpecific):
    ID = "stopForce"

    def __init__(self):
        super().__init__()

    def getID(self):
        return self.ID
    

    def getValues(self):
        ret = [HandsideToString(self._handSide), ActuationPointToString(self._actuationPoint)]
        return ret
    
    def setValues(self, values: list[str]):
        assert(len(values) == 2)
        self._handSide = StringToHandside(values[0])
        self._actuationPoint = StringToActuationPoint(values[1])

class SetTextureMessage(WeArtMessageObjectSpecific):
    ID = "texture"

    def __init__(self, idx:int, vel:float, vol:float):
        super().__init__()
        self._index = idx
        self._velocity = [0.5, 0.0, vel]
        self._volume = vol
    
    def getID(self):
        return self.ID

    def getValues(self):
        ret = []
        if (self._index < WeArtCommon.minTextureIndex or self._index > WeArtCommon.maxTextureIndex):
            self._index = WeArtCommon.nullTextureIndex
        
        ret.append(str(self._index))
        ret.append(str(self._velocity[0]))
        ret.append(str(self._velocity[1]))
        ret.append(str(self._velocity[2]))
        ret.append(str(self._volume))
        ret.append(HandsideToString(self._handSide))
        ret.append(ActuationPointToString(self._actuationPoint))
        return ret

    def setValues(self, values:list[str]):
        assert(len(values) == 6)
        self._index = int(values[0])
        self._velocity = []
        self._velocity.append(float(values[1]))
        self._velocity.append(float(values[2]))
        self._velocity.append(float(values[3]))
        self._volume = float(values[4])
        self._handSide = StringToHandside(values[5])
        self._actuationPoint = StringToActuationPoint(values[6])


class StopTextureMessage(WeArtMessageObjectSpecific):
    ID = "stopTexture"

    def __init__(self):
        super().__init__()

    def getID(self):
        return self.ID
    

    def getValues(self):
        ret = [HandsideToString(self._handSide), ActuationPointToString(self._actuationPoint)]
        return ret
    
    def setValues(self, values: list[str]):
        assert(len(values) == 2)
        self._handSide = StringToHandside(values[0])
        self._actuationPoint = StringToActuationPoint(values[1])
  



