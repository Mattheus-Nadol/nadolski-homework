"""
Module defining a hierarchy of musical instruments using inheritance.
"""
class Instrument:
    """Base class for all musical instruments"""
    def play(self) -> str:
        """Return a generic sound message"""
        return "Sound..."


class String(Instrument):
    """Represents string instruments"""
    def play(self) -> str:
        """Return sound message with string plucking"""
        return super().play() + "...plucking..."


class Wind(Instrument):
    """Represents wind instruments"""
    def play(self) -> str:
        """Return sound message with wind blowing"""
        return super().play() + "...blowing..."


class Guitar(String):
    """Represents a guitar instrument"""
    def play(self) -> str:
        """Return sound message with a D major chord"""
        return super().play() + "...D major chord"


class Trumpet(Wind):
    """Represents a trumpet instrument"""
    def play(self) -> str:
        """Return sound message with a high pitch note"""
        return super().play() + "...high pitch F6"


instruments:list = [
    Instrument(),
    String(),
    Wind(),
    Guitar(),
    Trumpet()
    ]

for instrument in instruments:
    print(instrument.play())
    print("-" * 10)
