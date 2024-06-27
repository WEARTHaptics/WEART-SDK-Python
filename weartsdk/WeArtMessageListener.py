from . import WeArtMessages as WeArtMessages

class WeArtMessageListener:
    def __init__(self, ids:list[str]):
        self._acceptedIds = ids

    def accept(self, id:str):
        if id in self._acceptedIds:
            return True
        else:
            return False
    def OnMessageReceived(message:WeArtMessages.WeArtMessage):
        return
