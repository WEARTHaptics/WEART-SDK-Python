import socket
import sys
import signal
import time
from threading import Thread
from enum import Enum

import WeArtCommon
from WeArtCommon import TrackingType
import WeArtMessage
from WeArtMessageSerializer import WeArtMessageSerializer
from  WeArtThimbleTrackingObject import WeArtThimbleTrackingObject
from WeArtMessageListener import WeArtMessageListener


class WeArtClient:
    messagesSeparator = '~'

    def __init__(self, ip_address, port):
        self._messageSerializer = WeArtMessageSerializer()
        self.__Connected = False
        self.__s = None #socket
        self.__thimbleTrackingObjects = []
        self.__messageListeners = []
        self.__connectionStatusCallbacks = []
        self.__errorCallbacks = []
        self.__pendingCallbacks = []
        self.__IP_ADDESS = ip_address
        self.__PORT = port

    class ErrorType(Enum):
        ConnectionError = 0
        SendMessageError = 1
        ReceiveMessageError = 2

    def Start(self, tracking_type = TrackingType.WEART_HAND):
        start_msg = None
        if tracking_type != None:
            start_msg = WeArtMessage.StartFromClientMessage(trackType=tracking_type)
        else:
            start_msg = WeArtMessage.StartFromClientMessage()
        self.SendMessage(start_msg)
        
    def Stop(self):
        stop_msg = WeArtMessage.StopFromClientMessage()
        self.SendMessage(stop_msg)
    
    def Run(self):
        try:
            self.__s = socket.socket()
            server_addr = (self.__IP_ADDESS, self.__PORT)
            self.__s.connect(server_addr)
            print(f"Connection to server: { server_addr } established.")
            self.__Connected = True
            self.__NotifyConnectionStatus(True)
            t = Thread(target=self._OnReceive, args = [], daemon=True)
            #t.run()
        except socket.error as e:
            print(f"Unable to connect to server { server_addr }... \n{e}")
            self.__Connected = False
            self.__NotifyError(self.ErrorType.ConnectionError)
            sys.exit()
        return
    
    def IsConnected(self):
        return self.__Connected
    
    def Close(self):
        return
    def StartCalibration(self):
        return
    def StopCalibration(self):
        return
    def SendMessage(self, msg:WeArtMessage.WeArtMessage):
        if not self.__Connected:
            return
        text = self._messageSerializer.Serialize(msg)
        text += self.messagesSeparator

        print(text)

        bytes = self.__s.send(text.encode())
        if bytes == 0:
            self.__Connected = False
            print("Send failed")
            self.__s.close()
            self.__NotifyError(self.ErrorType.SendMessageError)
            self.__NotifyConnectionStatus(False)
            return


    def AddThimbleTracking(self, trackingObjects: WeArtThimbleTrackingObject):
        return
    def SizeThimbles(self):
        return
    def AddMessageListener(self, listener: WeArtMessageListener):
        return
    def RemoveMessageListener(self, listener: WeArtMessageListener):
        return
    def AddConnectionStatusCallback(self, callback):
        return

    def AddErrorCallback(self, callback):
        return
    
    def _OnReceive(self):
        while True:
            data = self.__s.recv(4096)
            str_data = data.decode()
            print(str_data)
            strings = str_data.split(WeArtClient.messagesSeparator)
            messages = []
            for string in strings:
                messages.append(self._messageSerializer.Deserialize(string))
            self.__ForwardingMessages(messages)
        return
    
    def __ForwardingMessages(self, messages:list[WeArtMessage.WeArtMessage]):
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



if __name__ == '__main__':
    client = WeArtClient(WeArtCommon.DEFAULT_IP_ADDRESS, WeArtCommon.DEFAULT_TCP_PORT)
    client.Run()
    client.Start()
    client.Stop()