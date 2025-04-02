from .WeArtMessageListener import WeArtMessageListener
from .WeArtMessages import CalibrationResultMessage, CalibrationStatusMessage, WeArtMessage
from .WeArtCommon import CalibrationStatus, HandSide, CalibrationResult

class WeArtTrackingCalibration(WeArtMessageListener):
    """
    Represents a tracking calibration system that listens for calibration status and result messages.
    
    Attributes:
        __currentHand (HandSide): The current hand being calibrated (left or right).
        __status (CalibrationStatus): The calibration status.
        __result (int): The result of the calibration process (0 = success, 1 = failure).
        __statusCallbacks (list): A list of callbacks to be executed when the calibration status changes.
        __resultCallbacks (list): A list of callbacks to be executed when the calibration result changes.

    Methods:
        getCurrentHand: Returns the current hand being calibrated.
        getStatus: Returns the current calibration status.
        getResult: Returns the current calibration result.
        AddStatusCallback: Adds a callback function to be called when the calibration status changes.
        AddResultCallback: Adds a callback function to be called when the calibration result changes.
        OnMessageReceived: Handles incoming messages and updates the calibration status and result accordingly.
    """
    def __init__(self):
        """
        Initializes the WeArtTrackingCalibration instance with empty status and result, 
        and empty lists of callbacks.

        The constructor also sets up the message listener to handle the CalibrationStatusMessage 
        and CalibrationResultMessage types.
        """
        super().__init__([CalibrationStatusMessage.ID, CalibrationResultMessage.ID])
        self.__currentHand = None
        self.__status = None
        self.__result = False
        self.__statusCallbacks = []
        self.__resultCallbacks = []

    def getCurrentHand(self) -> HandSide:
        """
        Returns the current hand being calibrated.

        Returns:
            HandSide: The current hand (left or right).
        """
        return self.__currentHand
    
    def getStatus(self) -> CalibrationStatus:
        """
        Returns the current calibration status.
        Status can be one of the following:\n
        * "IDLE": The calibration process has started but is not yet running.
        * "Calibrating": The calibration process is running, the user has to keep the hand still.
        * "Running": The calibration process has successfully completed.

        Returns:
            CalibrationStatus: The current calibration status.
        """
        return self.__status
    
    def getResult(self) -> CalibrationResult:
        """
        Returns the current calibration result: 0 = success, 1 = failure.

        Returns:
            CalibrationResult: The result of the calibration process.
        """
        return self.__result
    
    def AddStatusCallback(self, callback):
        """
        Adds a callback function to be called when the calibration status changes.
        The callback function takes two parameters: handside and status.
        The callback signature is:\n
            def callback(handside: HandSide, status: CalibrationStatus)

        Parameters:
            callback (function): The callback function to be added.
        """
        self.__statusCallbacks.append(callback)
    
    def AddResultCallback(self, callback):
        """
        Adds a callback function to be called when the calibration result changes.
        The callback function takes two parameters: handside and result.
        The callback signature is:\n
            def callback(handside: HandSide, result: bool)
        """
        self.__resultCallbacks.append(callback)
    
    def OnMessageReceived(self, message: WeArtMessage):
        """
        Handles incoming messages related to calibration status and result.
        
        If the message is a CalibrationStatusMessage, updates the current hand and status, 
        and triggers the status callbacks.
        
        If the message is a CalibrationResultMessage, updates the current hand and result, 
        and triggers the result callbacks.

        Parameters:
            message (WeArtMessage): The received message.
        """
        if message.getID() == CalibrationStatusMessage.ID:
            self.__currentHand = message.getHand()
            self.__status = message.getStatus()
            for callback in self.__statusCallbacks:
                callback(self.__currentHand, self.__status)
        elif message.getID() == CalibrationResultMessage.ID:
            self.__currentHand = message.getHand()
            self.__result = message.getSuccess()
            for callback in self.__resultCallbacks:
                callback(self.__currentHand, self.__result)

__all__ = ['WeArtTrackingCalibration']
