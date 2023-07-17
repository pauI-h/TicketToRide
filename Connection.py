from City import City
from Colour import Colour


class Connection:

    def __init__(self, start: City, end: City, colour: Colour, length: int, tunnel: bool,
                 num_locomotives: int):
        self.__start = start
        self.__end = end
        self.__colour = colour
        self.__length = length
        self.__used = None
        self.__tunnel = tunnel
        self.__locomotives = num_locomotives

    def getLocations(self):
        return self.__start, self.__end

    def getController(self):
        return self.__used

    def getColourAndLength(self):
        return self.__colour, self.__length

    def getLength(self):
        return self.__length

    def isTunnel(self):
        return self.__tunnel

    def getLocomotives(self):
        return self.__locomotives

    def use(self, hand: dict, colour, deck, player):
        if colour != self.__colour and self.__colour != Colour.ANY:
            # Checks the right colour is being used
            return False, -1, -1

        needed = self.__length

        if self.__tunnel:  # Adds the extra trains demanded by the tunnel
            for i in range(3):
                new = deck.deal()
                if new == colour or new == Colour.ANY:
                    needed += 1

        if hand[Colour.ANY] < self.__locomotives:  # Checks enough locomotives
            return False, -2, self.__locomotives

        num_normal = hand[colour]
        loco_needed = self.__locomotives
        norm_used = needed

        if num_normal < needed - self.__locomotives:  # If not enough normal use extra locomotives
            loco_needed += (needed - self.__locomotives) - num_normal
            norm_used = num_normal

        if hand[Colour.ANY] < loco_needed:  # If not enough locomotives cannot complete
            return False, needed, self.__locomotives

        self.__used = player
        return True, norm_used, loco_needed

    def __str__(self):
        state = "Empty"
        tunnel = ""
        if self.__used:
            state = "Full "
        if self.__tunnel:
            tunnel = "Tunnel "
        return str(self.__start) + "->" + str(self.__end) + ", " + str(self.__colour) + " " + \
               tunnel + str(self.__length) + " Locomotives = " + str(self.__locomotives) + \
               " State = " + state
