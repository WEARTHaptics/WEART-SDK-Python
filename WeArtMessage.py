from WeArtCommon import TrackingType, HandSide, ActuationPoint
import WeArtCommon

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

    def setHandSide(self, handside):
        return

    def setActuationPoint(self, actuation_point):
        return



class WeArtMessageNoParams(WeArtMessage):
   
    # the message carries no value, so return empty list
    def getValues(self):
        return []
    # the message carries no value, so return without doint anything
    def setValues(self, values):
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
            ret.append(self.__RightThumbClosure)
            ret.append(self.__RightIndexClosure)
            ret.append(self.__RightMiddleClosure)
            ret.append(self.__RightPalmClosure)
            ret.append(self.__LeftThumbClosure)
            ret.append(self.__LeftIndexClosure)
            ret.append(self.__LeftMiddleClosure)
            ret.append(self.__LeftPalmClosure)
        elif self._trackingType == TrackingType.WEART_HAND:
            ret.append(self.__RightIndexClosure)
            ret.append(self.__RightThumbClosure)
            ret.append(self.__RightThumbAbduction)
            ret.append(self.__RightMiddleClosure)
            
            ret.append(self.__LeftIndexClosure)
            ret.append(self.__LeftThumbClosure)
            ret.append(self.__LeftThumbAbduction)
            ret.append(self.__LeftMiddleClosure)
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



