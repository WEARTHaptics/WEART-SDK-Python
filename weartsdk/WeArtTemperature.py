class WeArtTemperature:
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
    def value(self, temperature:float):
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
