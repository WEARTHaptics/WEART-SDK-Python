import socket
import sys
from threading import Thread
from enum import Enum
import logging

from .WeArtCommon import TrackingType
from . import WeArtMessages as WeArtMessages
from .WeArtMessageSerializer import WeArtMessageSerializer
from  .WeArtThimbleTrackingObject import WeArtThimbleTrackingObject
from .WeArtMessageListener import WeArtMessageListener


logging.basicConfig()

class WeArtClient:
    """
    A client class to communicate with a server using socket connections. 
    The client can send and receive messages, handle connections, and track thimbles. 

    Attributes:
        messagesSeparator (str): The separator used to delimit messages.
    """
    messagesSeparator = '~'

    def __init__(self, ip_address, port, log_level = logging.DEBUG):
        """
        Initializes a WeArtClient instance.

        :param ip_address: The IP address of the server to connect to.
        :param port: The port number to use for the connection.
        :param log_level: The logging level (default is logging.DEBUG).
        """
        self._messageSerializer = WeArtMessageSerializer()
        self.__Connected = False
        self.__Closing = False
        self.__s = None #socket
        self.__thimbleTrackingObjects = []
        self.__messageListeners = []
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
        """
        Sends a start message to connected device(s) based on the tracking type.

        :param tracking_type: The tracking type to use (default is WEART_HAND).
        """
        start_msg = None
        if tracking_type != None:
            start_msg = WeArtMessages.StartFromClientMessage(trackType=tracking_type)
        else:
            start_msg = WeArtMessages.StartFromClientMessage()
        self._sendMessage(start_msg)
        
    def Stop(self):
        """
        Sends a stop message to connected device(s).
        """
        stop_msg = WeArtMessages.StopFromClientMessage()
        self._sendMessage(stop_msg)
    
    def Run(self):
        """
        Establishes a socket connection with the Middleware or WeArtApp.
        """
        try:
            self.__s = socket.socket()
            server_addr = (self.__IP_ADDRESS, self.__PORT)
            self.__s.connect(server_addr)
            self.__logger.info(f"Connection to server: { server_addr } established.")
            self.__Connected = True
            self.__NotifyConnectionStatus(True)
            t = Thread(target=self._OnReceive, args = [], daemon=True)
            t.start()

        except socket.error as e:
            self.__logger.error(f"Unable to connect to server { server_addr }... \n{e}")
            self.__Connected = False
            self.__NotifyError(self.ErrorType.ConnectionError)
            sys.exit()
        
        return
    
    def IsConnected(self):
        """
        Checks if the Middleware or the WeArtApp is connected.

        :return: True if connected, False otherwise.
        """
        return self.__Connected
    
    def Close(self):
        """
        Closes the socket connection with the Middleware or WeArtApp.
        """
        self.__Closing = True
        self.__s.close()
        self.__Connected = False
        self.__NotifyConnectionStatus(False)

    def StartCalibration(self):
        """
        Starts the calibration process.
        """
        startCalibration = WeArtMessages.StartCalibrationMessage()
        self._sendMessage(startCalibration)

    def StopCalibration(self):
        """"
        Stops the calibration process.
        """
        stopCalibration = WeArtMessages.StopCalibrationMessage()
        self._sendMessage(stopCalibration)

    def StartRawData(self):
        """"
        Starts the raw data collection from the device(s).
        """
        message = WeArtMessages.RawDataOn()
        self._sendMessage(message)

    def StopRawData(self):
        """""
        Stops the raw data collection from the device(s).
        """
        message = WeArtMessages.RawDataOff()
        self._sendMessage(message)
    
    def AddThimbleTracking(self, trackingObject: WeArtThimbleTrackingObject):
        """
        Adds a thimble tracking object to the list of tracked thimbles.
        Once a thimble tracking object is added, the client will start receiving tracking data from the device(s).
        
        :param trackingObjects: The WeArtThimbleTrackingObject to add.
        """
        self.__thimbleTrackingObjects.append(trackingObject)
        self.AddMessageListener(trackingObject)

    def RemoveThimbleTracking(self, trackingObject: WeArtThimbleTrackingObject):
        """
        Removes a thimble tracking object from the list of tracked thimbles.
        Once a thimble tracking object is removed, the client will stop receiving tracking data from the device(s).

        :param trackingObjects: The WeArtThimbleTrackingObject to remove.
        """
        if trackingObject in self.__thimbleTrackingObjects:
            self.__thimbleTrackingObjects.remove(trackingObject)

    def ThimbleTrackingObjectsSize(self):
        """
        Returns the number of thimble tracking objects currently being tracked.

        :return: The number of thimble tracking objects.
        """
        return len(self.__thimbleTrackingObjects)
    
    def AddMessageListener(self, listener: WeArtMessageListener):
        """
        Adds a message listener to the list of message listeners.
        A message listener handles incoming messages from the Middleware or WeArtApp anddevice(s).
        \nYou can add:
            * MiddlewareStatusListener: to receive Middleware or WeArtApp status messages.
            * DeviceStatusListener: to receive TouchDiver device(s) status messages.
            * TDProStatusListener: to receive TouchDiver Pro device(s) status messages.
            * WeArtTrackingCalibration: to receive calibration status messages.
            * WeArtTrackingRawData: to receive raw data from device(s).

        :param listener: The WeArtMessageListener to add.
        """
        self.__messageListeners.append(listener)

    def RemoveMessageListener(self, listener: WeArtMessageListener):
        '''
        Removes a message listener from the list of message listeners.

        :param listener: The WeArtMessageListener to remove.
        '''
        if listener in self.__messageListeners:
            self.__messageListeners.remove(listener)

    def AddConnectionStatusCallback(self, callback):
        '''
        Adds a callback function to be called when the connection status changes.
        The callback function should take a boolean parameter indicating the new connection status: True if connected, False otherwise.

        :param callback: The callback function to be called.
        '''
        self.__connectionStatusCallbacks.append(callback)

    def AddErrorCallback(self, callback):
        '''
        Adds a callback function to be called when an error occurs.
        The callback function should take a :class:`ErrorType` parameter indicating the error.

        :param callback: The callback function to be called.
        '''
        self.__errorCallbacks.append(callback)
    
    def _sendMessage(self, msg: WeArtMessages.WeArtMessage):
        """
        Sends a serialized message to the server.

        :param msg: The message to be sent.
        """
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

    def _OnReceive(self):
        '''
        Handles incoming messages from the server.
        '''
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
    
    def __ForwardingMessages(self, messages: list[WeArtMessages.WeArtMessage]):
        '''
        Forwards messages to the message listener(s).
        '''
        for msg in messages:
            if msg == None:
                continue
            for listener in self.__messageListeners:
                if (listener.accept(msg.getID())):
                    listener.OnMessageReceived(msg)
    
    def __NotifyConnectionStatus(self, connected: bool):
        '''
        Notifies the connection status to the connection status callback(s).
        '''
        for callback in self.__connectionStatusCallbacks:
            t = Thread(target=callback, args = [connected])
            t.start()
            self.__pendingCallbacks.append(t)
        self.__ClearProcessedCallbacks()
    
    def __NotifyError(self, errorType: ErrorType):
        '''
        Notifies the error to the error callback(s).
        '''
        for callback in self.__errorCallbacks:
            t = Thread(target=callback, args = [errorType])
            t.start()
            self.__pendingCallbacks.append(t)
        self.__ClearProcessedCallbacks()
    
    def __ClearProcessedCallbacks(self):
        ''''
        Clears the processed callbacks.
        '''
        for t in self.__pendingCallbacks:
            t.join()

__all__ = ['WeArtClient']