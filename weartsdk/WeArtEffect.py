from .WeArtTemperature import WeArtTemperature
from .WeArtForce import WeArtForce
from .WeArtTexture import WeArtTexture

class WeArtEffect:
    """
    Base class for different types of effects.

    This class defines the basic structure for effects that can provide temperature,
    force, and texture information. Derived classes must implement specific behaviors.
    """
    def __init__(self):
        return
    
    def getTemperature():
        return
    
    def getForce():
        return
    
    def getTexture():
        return

class TouchEffect(WeArtEffect):
    """
    Represents a touch effect that includes temperature, force, and texture information.

    This class extends the WeArtEffect class and allows the manipulation and retrieval
    of the temperature, force, and texture properties.

    Attributes:
        __temperature (WeArtTemperature): The temperature associated with the touch effect.
        __force (WeArtForce): The force associated with the touch effect.
        __texture (WeArtTexture): The texture associated with the touch effect.
    """
    def __init__(self, temp: WeArtTemperature, force: WeArtForce, texture: WeArtTexture):
        """
        Initializes the TouchEffect object with specific temperature, force, and texture.

        Args:
            temp (WeArtTemperature): The temperature associated with the effect.
            force (WeArtForce): The force associated with the effect.
            texture (WeArtTexture): The texture associated with the effect.
        """
        self.__temperature = temp
        self.__force = force
        self.__texture = texture

    def getTemperature(self):
        return self.__temperature

    def getForce(self):
        return self.__force
    
    def getTexture(self):
        return self.__texture
    
    def Set(self, temperature: WeArtTemperature, force: WeArtForce, texture: WeArtTexture):
        """
        Sets new values for temperature, force, and texture for the touch effect.
        Returns a boolean indicating whether any changes were made.

        Args:
            temperature (WeArtTemperature): The new temperature to be set.
            force (WeArtForce): The new force to be set.
            texture (WeArtTexture): The new texture to be set.

        Returns:
            bool: True if any of the values were changed, otherwise False.
        """
        changed = False

        if temperature != self.__temperature:
            changed = True
            self.__temperature = temperature

        if force != self.__force:
            changed = True
            self.__force = force

        if texture != self.__texture:
            changed = True
            texture.textureVelocity = 0.5
            self.__texture = texture

        return changed

__all__ = ['WeArtEffect', 'TouchEffect']
