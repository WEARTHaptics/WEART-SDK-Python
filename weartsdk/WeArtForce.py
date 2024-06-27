class WeArtForce:
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
    def value(self, force:float):
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
