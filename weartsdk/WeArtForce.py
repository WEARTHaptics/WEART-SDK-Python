class WeArtForce:
    """
    A class representing the force applied in a touch interaction.

    Attributes:
        DefaultValue (float): The default value for the force, set to 0.5.
        MinValue (float): The minimum allowed value for the force, set to 0.0.
        MaxValue (float): The maximum allowed value for the force, set to 1.0.
        active (bool): A flag indicating whether the force is active or not.
        value (float): The force value, constrained within the range [MinValue, MaxValue].

    Methods:
        __init__(self, active: bool = False, force: float = 0.5):
            Initializes the force with the specified active state and force value.
        
        value (property):
            Getter for the force value.
            Setter for the force value, ensuring it stays within the valid range [MinValue, MaxValue].

        __eq__(self, other):
            Compares two WeArtForce objects to check if they are equal based on their active state and force value.
    """
    DefaultValue = 0.5
    MinValue = 0.0
    MaxValue = 1.0

    def __init__(self, active = False, force = 0.5):
        self.active = active
        self.__value = force
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, force: float):
        if force < self.MinValue:
            self.__value = self.MinValue
        elif force > self.MaxValue:
            self.__value = self.MaxValue
        else:
            self.__value = force

    def __eq__(self, other):
        if (self.active == other.active and self.__value == other.value):
            return True
        else:
            return False

__all__ = ['WeArtForce']
