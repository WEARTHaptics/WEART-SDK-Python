class WeArtTemperature:
    """
    Represents a temperature value with a configurable range and an active state.
    
    Attributes:
        DefaultValue (float): The default temperature value (0.5).
        MinValue (float): The minimum allowable temperature (0.0).
        MaxValue (float): The maximum allowable temperature (1.0).
        active (bool): Indicates whether the temperature effect is active.
        __value (float): The actual temperature value, constrained within the allowed range.

    Methods:
        value: Gets or sets the temperature value, ensuring it stays within the MinValue and MaxValue.
        __eq__: Compares two WeArtTemperature objects for equality based on their active state and value.
    """
    DefaultValue = 0.5
    MinValue = 0.0
    MaxValue = 1.0

    def __init__(self):
        self.active = False
        self.__value = self.DefaultValue
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, temperature: float):
        if temperature < self.MinValue:
            self.__value = self.MinValue
        elif temperature > self.MaxValue:
            self.__value = self.MaxValue
        else:
            self.__value = temperature

    def __eq__(self, other):
        if (self.active == other.active and self.__value == other.value):
            return True
        else:
            return False

__all__ = ['WeArtTemperature']
