"""Provides a TV class with encapsulated state and basic control methods."""
from typing import Union

class TV:
    """Represents a TV with channel, volume, and power state control."""
    def __init__(self, channel:int=1, volume:int=10, is_active:bool=False) -> None:
        self._channel = channel
        self._volume = volume
        self.__active = is_active

    def activate(self) -> bool:
        """Turns the TV on."""
        self.__active = True
        return self.__active

    def deactivate(self) -> bool:
        """Turns the TV off."""
        self.__active = False
        return self.__active

    def change_channel(self, number:int) -> Union[int, str]:
        """Changes the channel if the TV is on."""
        if self.__active is True:
            self._channel = number
            return self._channel
        return "Cannot change the channel with TV off"

    def turn_up(self, grade:int) -> Union[int, str]:
        """Increases volume by a given amount if the TV is on and within range."""
        if self.__active is True:
            if self._volume + grade <= 100:
                self._volume += grade
                return self._volume
            return "Unable to turn up the volume above 100"
        return "Cannot change the volume with TV off"

    def turn_down(self, grade:int) -> Union[int, str]:
        """Decreases volume by a given amount if the TV is on and within range."""
        if self.__active is True:
            if self._volume - grade >= 0:
                self._volume -= grade
                return self._volume
            return "Unable to turn down the volume below 0"
        return "Cannot change the volume with TV off"

    @property
    def info(self) -> str:
        """Displays the current TV status."""
        return f"STATUS:\nActive: {self.__active}\nChannel: {self._channel}\nVolume: {self._volume}"


#Test cases
switch = TV() # With default settings
print("1.", switch.info) # Current status

switch.turn_up(12) # Attempt to change che volume up
print("2.", switch.info) # Volume remains 10

switch.change_channel(4) # Attempt to switch channel
print("3.", switch.info) # Channel remains 1

switch.__active = True # Attempt of incorrect TV activate (ON PURPOSE)
print("4.", switch.info) # TV remains off

switch.activate() # Turning the TV on
print("5.", switch.info) # TV is turned on

switch.change_channel(5)
switch.turn_up(20) # Volume increased by 20 (expected 30)
print("6.", switch.info) # channel changed, volume increased

switch.turn_up(80) #Attempt of turning up by 80 (expected 110)
print("7.", switch.info) # volume remains 30
