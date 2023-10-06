import warnings

from Deck import Deck
from Players.DumbPlayer import DumbPlayer
from Route import Route


class TestPlayer(DumbPlayer):

    def __init__(self, trains: int, flight_trains: int, deck: Deck):
        super().__init__(trains, flight_trains, deck)
        warnings.warn("This is for testing use only")

    def addRoute(self, route: Route):
        self._routes.append(route)

    def placeTrain(self, connection, colour):
        self._tryPlace(connection, colour)
