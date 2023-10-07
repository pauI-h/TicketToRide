from abc import ABC, abstractmethod

from Colour import Colour
from Deck import Deck
from Exceptions import NotEnoughCardsException, WrongColourException, NotEnoughLocomotivesException, \
    NotEnoughPiecesException, ParallelConnectionException


class Player(ABC):

    def __init__(self, trains: int, flight_trains: int, deck: Deck):
        self.__controlled_routes = []
        self.__hand = {}
        self._routes = []
        self.__trains = trains
        self.__flight_trains = flight_trains
        self.__deck = deck
        self.__locations = set()
        self.__location_pairs = []
        for colour in Colour:
            self.__hand[colour] = 0

    @property
    def routes(self):
        return self._routes.copy()  # Copy stops pass by reference edits

    @property
    def hand(self):
        return self.__hand.copy()  # Copy stops pass by reference edits

    @property
    def locations(self):
        return self.__locations.copy()  # Copy stops editing using pass by reference

    def addToHand(self, colour):
        self.__hand[colour] += 1

    def _tryPlace(self, connection, colour) -> Exception:
        """
        Attempts to place a route and if successful removes the resources required
        :param connection: The connection to try and place
        :param colour: The colour of card to use
        :return: An exception describing the issue if unable to complete, else none
        """
        if not connection.flight_connection and connection.getLength() > self.__trains:
            return NotEnoughPiecesException("Trains")
        elif connection.flight_connection and connection.getLength() > self.__flight_trains:
            return NotEnoughPiecesException("Flight")

        if (connection.getLocations()) in self.__location_pairs:
            return ParallelConnectionException("Already control parallel route")

        result, norm_used, loco_used = connection.use(self.__hand, colour, self.__deck, self)

        if result:
            self.__hand[colour] -= norm_used
            self.__hand[Colour.ANY] -= loco_used
            # Updates the locations connected by the player
            self.__locations.add(connection.getLocations()[0])
            self.__locations.add(connection.getLocations()[1])
            if connection.flight_connection:
                self.__flight_trains -= connection.getLength()
            else:
                self.__trains -= connection.getLength()

            self.__location_pairs.append((connection.getLocations()))

            return None

        else:
            if (norm_used, loco_used) == (-1, -1):
                return WrongColourException("Wrong Colour Used")
            elif norm_used == -2:
                return NotEnoughLocomotivesException("Not Enough Locomotives")
            else:
                return NotEnoughCardsException("Not enough cards")

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
