import socket
import sys
import signal
import time
from threading import Thread
from enum import Enum
import logging

from . import WeArtCommon
from .WeArtCommon import TrackingType
from . import WeArtMessages as WeArtMessages
from .WeArtMessageSerializer import WeArtMessageSerializer
from  .WeArtThimbleTrackingObject import WeArtThimbleTrackingObject
from .WeArtMessageListener import WeArtMessageListener
from .WeArtTrackingRawData import WeArtTrackingRawData
from .WeArtAnalogSensorData import WeArtAnalogSensorData


logging.basicConfig()

class WeArtClient:
    messagesSeparator = '~'

    def __init__(self, ip_address, port, log_level = logging.DEBUG):
        self._messageSerializer = WeArtMessageSerializer()
        self.__Connected = False
        self.__Closing = False
        self.__s = None #socket
        self.__thimbleTrackingObjects = []
        self.__messageListeners = []
        self.__messageCallbacks = []
        self.__connectionStatusCallbacks = []
        self.__errorCallbacks = []
        self.__pendingCallbacks = []
        self.__IP_ADDRESS = ip_address
        self.__PORT = port
        self.__logger = logging.getLogger("WeArtClient")
        self.__logger.setLevel(log_level)

    class ErrorType(Enum):
        ConnectionError = 0
        SendMessageError = 1
        ReceiveMessageError = 2

    def Start(self, tracking_type = TrackingType.WEART_HAND):
        start_msg = None
        if tracking_type != None:
            start_msg = WeArtMessages.StartFromClientMessage(trackType=tracking_type)
        else:
            start_msg = WeArtMessages.StartFromClientMessage()
        self.SendMessage(start_msg)
        
    def Stop(self):
        stop_msg = WeArtMessages.StopFromClientMessage()
        self.SendMessage(stop_msg)
    
    def Run(self):
        try:
            self.__s = socket.socket()
            server_addr = (self.__IP_ADDRESS, self.__PORT)
            self.__s.connect(server_addr)
            self.__logger.info(f"Connection to server: { server_addr } established.")
            self.__Connected = True
            self.__NotifyConnectionStatus(True)
            t = Thread(target=self._OnReceive, args = [], daemon=True)
            t.start()

            #getStatusMessage = WeArtMessages.GetMiddlewareStatus()
            #self.SendMessage(getStatusMessage)

            getDevicesMessage = WeArtMessages.GetDevicesStatusMessage()
            self.SendMessage(getDevicesMessage)

        except socket.error as e:
            self.__logger.error(f"Unable to connect to server { server_addr }... \n{e}")
            self.__Connected = False
            self.__NotifyError(self.ErrorType.ConnectionError)
            sys.exit()
        return
    
    def IsConnected(self):
        return self.__Connected
    
    def Close(self):
        self.__Closing = True
        self.__s.close()
        self.__Connected = False
        self.__NotifyConnectionStatus(False)

    def StartCalibration(self):
        startCalibration = WeArtMessages.StartCalibrationMessage()
        self.SendMessage(startCalibration)

    def StopCalibration(self):
        stopCalibration = WeArtMessages.StopCalibrationMessage()
        self.SendMessage(stopCalibration)

    def StartRawData(self):
        message = WeArtMessages.RawDataOn()
        self.SendMessage(message)

    def StopRawData(self):
        message = WeArtMessages.RawDataOff()
        self.SendMessage(message)
    
    def SendMessage(self, msg:WeArtMessages.WeArtMessage):
        if not self.__Connected:
            return
        if msg == None:
            return
        
        text = msg.serialize()
        text+= self.messagesSeparator

        self.__logger.debug(f"Message to be sent: { text }")

        bytes = self.__s.send(text.encode())
        if bytes == 0:
            self.__Connected = False
            self.__logger.error(f"Send message '{ text }' failed")
            self.__s.close()
            self.__NotifyError(self.ErrorType.SendMessageError)
            self.__NotifyConnectionStatus(False)
            return


    def AddThimbleTracking(self, trackingObjects: WeArtThimbleTrackingObject):
        self.__thimbleTrackingObjects.append(trackingObjects)
        self.AddMessageListener(trackingObjects)

    def AddThimbleRawSensors(self, rawSensorData: WeArtTrackingRawData):
        return
    
    def AddThimbleAnalogRawSensor(self, analogRawSensorData: WeArtAnalogSensorData):
        return
        
    def SizeThimbles(self):
        return len(self.__thimbleTrackingObjects)
    
    def AddMessageListener(self, listener: WeArtMessageListener):
        self.__messageListeners.append(listener)

    def AddMessageCallback(self, callback):
        return

    def RemoveMessageListener(self, listener: WeArtMessageListener):
        if listener in self.__messageListeners:
            self.__messageListeners.remove(listener)

    def RemoveMessageCallback(self, callback):
        return

    def AddConnectionStatusCallback(self, callback):
        self.__connectionStatusCallbacks.append(callback)

    def AddErrorCallback(self, callback):
        self.__errorCallbacks.append(callback)
    
    def _OnReceive(self):
        try:
            while True:
                data = self.__s.recv(4096)
                str_data = data.decode()
                self.__logger.debug(f"Received: { str_data }")
                strings = str_data.split(WeArtClient.messagesSeparator)
                messages = []
                for string in strings:
                    messages.append(self._messageSerializer.Deserialize(string))
                self.__ForwardingMessages(messages)
        except Exception:
            if not self.__Closing:
                raise
    
    def __ForwardingMessages(self, messages:list[WeArtMessages.WeArtMessage]):
        for msg in messages:
            if msg == None:
                continue
            for listener in self.__messageListeners:
                if (listener.accept(msg.getID())):
                    listener.OnMessageReceived(msg)
    
    def __NotifyConnectionStatus(self, connected:bool):
        for callback in self.__connectionStatusCallbacks:
            t = Thread(target=callback, args = [connected])
            t.start()
            self.__pendingCallbacks.append(t)
        self.__ClearProcessedCallbacks()
    
    def __NotifyError(self, errorType:ErrorType):
        for callback in self.__errorCallbacks:
            t = Thread(target=callback, args = [errorType])
            t.start()
            self.__pendingCallbacks.append(t)
        self.__ClearProcessedCallbacks()
    
    def __ClearProcessedCallbacks(self):
        for t in self.__pendingCallbacks:
            t.join()

__all__ = ['WeArtClient']