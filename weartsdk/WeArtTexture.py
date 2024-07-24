from .WeArtCommon import TextureType

class WeArtTexture:
    DefaultTextureType = TextureType.ClickNormal
    
    DefaultVolume = 100.0
    MinVolume = 0.0
    MaxVolume = 100.0

    DefaultVelocity = 0.0
    MinVelocity = 0.0
    MaxVelocity = 0.5

    def __init__(self, active = False, texture_type = TextureType.ClickNormal, velocity = 0.0, volume = 100.0):
        self.active = active
        self.__textureType = texture_type
        self.__textureVelocity = velocity
        self.__volume = volume
    
    @property
    def textureVelocity(self):
        return self.__textureVelocity
    
    @textureVelocity.setter
    def textureVelocity(self, velocity:float):
        if velocity < self.MinVelocity:
            self.__textureVelocity = self.MinVelocity
        elif velocity > self.MaxVelocity:
            self.__textureVelocity = self.MaxVelocity
        else:
            self.__textureVelocity = velocity

    @property
    def textureType(self):
        return self.__textureType
    
    @textureType.setter
    def textureType(self, texture_type:TextureType):
        lower = TextureType.ClickNormal
        upper = TextureType.DoubleSidedTape

        if texture_type.value <= lower.value:
            self.__textureType = lower
        elif texture_type.value >= upper.value:
            self.__textureType = upper
        else:
            self.__textureType = texture_type
    
    @property
    def volume(self):
        return self.__volume
    
    @volume.setter
    def volume(self, volume:float):
        if volume < self.MinVolume:
            self.__volume = self.MinVolume
        elif volume > self.MaxVolume:
            self.__volume = self.MaxVolume
        else:
            self.__volume = volume

    def __eq__(self, other):
        if (self.active == other.active and self.__textureType == other.textureType and self.__textureVelocity == other.textureVelocity and self.__volume == other.volume):
            return True
        else:
            return False
    
__all__ = ['WeArtTexture']
