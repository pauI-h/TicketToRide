from enum import Enum


class Colour(Enum):
    RED = "Red"
    WHITE = "White"
    BLACK = "Black"
    YELLOW = "Yellow"
    PINK = "Pink"
    ORANGE = "Orange"
    BLUE = "Blue"
    GREEN = "Green"
    ANY = "Any"

    def __str__(self):
        return str(self.value)
