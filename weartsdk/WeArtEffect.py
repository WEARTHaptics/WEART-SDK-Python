from .WeArtTemperature import WeArtTemperature
from .WeArtForce import WeArtForce
from .WeArtTexture import WeArtTexture

class WeArtEffect:
    def __init__(self):
        return
    
    def getTemperature():
        return
    def getForce():
        return
    def getTexture():
        return

class TouchEffect(WeArtEffect):
    def __init__(self, temp:WeArtTemperature, force:WeArtForce, texture:WeArtTexture):
        self.__temperature = temp
        self.__force = force
        self.__texture = texture

    def getTemperature(self):
        return self.__temperature

    def getForce(self):
        return self.__force
    
    def getTexture(self):
        return self.__texture
    
    def Set(self, temperature:WeArtTemperature, force:WeArtForce, texture = WeArtTexture):
        changed = False

        if temperature == self.__temperature:
            changed = True
        self.__temperature = temperature

        if force == self.__force:
            changed = True
        self.__force = force

        if texture == self.__texture:
            changed = True
        texture.textureVelocity = 0.5
        self.__texture = texture

        return changed

__all__ = ['WeArtEffect', 'TouchEffect']
