from abc import ABC, abstractmethod

from Colour import Colour
from Deck import Deck


class Player(ABC):

    def __init__(self, trains: int, deck: Deck):
        self.__controlled_routes = []
        self.__hand = {}
        self._routes = []
        self.__trains = trains
        self.__deck = deck
        self.__colour_pos_map = deck.getColourPosMap()
        self.__locations = set()
        for colour in Colour:
            self.__hand[colour] = 0

    @property
    def routes(self):
        return self._routes

    def add_to_hand(self, colour):
        self.__hand[colour] += 1

    def getRoutes(self):
        return self._routes

    def getLocations(self):
        return self.__locations.copy()  # Copy stops editing using pass by reference

    def _tryPlace(self, connection, colour):
        if connection.getLength() > self.__trains:
            return

        result, norm_used, loco_used = connection.use(self.__hand, colour, self.__deck, self)
        if result:
            self.__hand[colour] -= norm_used
            self.__hand[Colour.ANY] -= loco_used
            # Updates the locations connected by the player
            self.__locations.add(connection.getLocations()[0])
            self.__locations.add(connection.getLocations()[1])
            self.__trains -= connection.getLength()

    @abstractmethod
    def drawCardTurn(self, map_rep) -> int:
        """
        Draws cards from either the deck or board
        :param map_rep:
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def pickRouteTurn(self, map_rep) -> int:
        """
        Picks routes from the pile
        :param map_rep:
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def placeTrainTurn(self, map_rep, connections) -> int:
        """
        Places Trains on the map
        :param map_rep:
        :param connections:
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def pickAction(self, map_rep, connections) -> (int, int):
        """
        Picks which action to do from: place train, draw cards, draw routes
        :param map_rep:
        :param connections:
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def calculateMapRep(self, connections):
        """
        Calculated the map representation used by the model
        :param connections:
        :return:
        """
        raise NotImplemented

    def turn(self, connections) -> (int, int):
        map_rep = self.calculateMapRep(connections)
        return self.pickAction(map_rep, connections)
