from . import WeArtMessages as WeArtMessages

class WeArtMessageListener:
    """
    A class for listening to and accepting messages based on predefined IDs.
    """
    def __init__(self, ids: list[str]):
        """
        Initializes a WeArtMessageListener with the given list of accepted message IDs.
        
        Parameters:
            ids (list[str]): A list of message IDs that this listener will accept.
        """
        self._acceptedIds = ids

    def accept(self, id: str):
        """
        Checks whether a given message ID is accepted by this listener.

        Parameters:
            id (str): The message ID to check.
        
        Returns:
            bool: True if the ID is accepted, False otherwise.
        """
        if id in self._acceptedIds:
            return True
        else:
            return False
    
    def OnMessageReceived(message: WeArtMessages.WeArtMessage):
        """
        A method to be triggered when a message is received. The implementation of this method should 
        be provided by a subclass or instance using this listener.
        
        Parameters:
            message (WeArtMessages.WeArtMessage): The message that has been received.
        """
        return
